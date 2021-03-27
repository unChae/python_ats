import json
import boto3
import datetime
import io
import pandas as pd
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests

import pymysql
from pymysql.cursors import DictCursor

# call .env
from dotenv import load_dotenv

load_dotenv(verbose=True)
server_url = os.getenv('URL')
client = boto3.client('s3')

#db 연결
conn = pymysql.connect(
  user=os.getenv('DATABASE_USER'), 
  passwd=os.getenv('DATABASE_PASSWORD'), 
  host=os.getenv('DATABASE_HOST'), 
  db=os.getenv('DATABASE_NAME'), 
  charset='utf8',
  cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()

# 중복 함수
def get_setting_data():
  query = '''
    SELECT * 
    FROM Settings;
  '''
  cursor.execute(query)
  return cursor.fetchall()
  
def get_market_code(market_code):
  query = '''
    SELECT * 
    FROM Markets
    WHERE market_code = %s;
  '''
  cursor.execute(query, market_code)
  return cursor.fetchone()
  
def get_user_key(user_id):
  query = '''
    SELECT * 
    FROM ApiKeys
    WHERE user_id = %s;
  '''
  cursor.execute(query, user_id)
  return cursor.fetchone()
  
def get_user_asset(market, key):
  payload = {
    'access_key': key['access_key'],
    'nonce': str(uuid.uuid4()),
  }
  jwt_token = jwt.encode(payload, key['secret_key'])
  authorize_token = 'Bearer {}'.format(jwt_token)
  headers = {"Authorization": authorize_token}
  data = requests.get(server_url + "/v1/accounts", headers=headers).json()
  for item in data:
    if item.get('currency') == market:
      data = item.get('balance')
  return data
  
def get_user_trade_price(market, key):
  payload = {
    'access_key': key['access_key'],
    'nonce': str(uuid.uuid4()),
  }
  jwt_token = jwt.encode(payload, key['secret_key'])
  authorize_token = 'Bearer {}'.format(jwt_token)
  headers = {"Authorization": authorize_token}
  data = requests.get(server_url + "/v1/accounts", headers=headers).json()
  for item in data:
    if item.get('currency') == market:
      data = item.get('avg_buy_price')
  print('----')
  print(market)
  print(data)
  print('----')
  return data
  
# 도형 함수
def get_trade_data() : 
  query = '''
    SELECT * 
    FROM Trades;
  '''
  cursor.execute(query)
  return cursor.fetchall()
  
def get_setting_benefit(user_id, setting_id) :
  query = '''
    SELECT *
    FROM Settings
    WHERE user_id = %s AND setting_id = %s
  '''
  payload = (user_id, setting_id)
  cursor.execute(query, payload)
  return cursor.fetchall()

def get_market_name(market_id) :
  query = '''
    SELECT *
    FROM Markets
    WHERE market_id = %s
  '''
  cursor.execute(query, market_id)
  return cursor.fetchone()
  
#매도
def sell_order(market, asset_data, key):
  query = {
    'market': market,
    'side': 'ask',
    'volume': asset_data,
    'ord_type': 'market',
  }
  query_string = urlencode(query).encode()

  m = hashlib.sha512()
  m.update(query_string)
  query_hash = m.hexdigest()

  payload = {
    'access_key': key['access_key'],
    'nonce': str(uuid.uuid4()),
    'query_hash': query_hash,
    'query_hash_alg': 'SHA512',
  }
  
  jwt_token = jwt.encode(payload, key['secret_key'])
  authorize_token = 'Bearer {}'.format(jwt_token)
  headers = {"Authorization": authorize_token}
  res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
  print(res.json())
  
# 매도 후 trade_status 0으로 바꿈
def set_trade_status(user_id, setting_id, market_id) :
  query = '''
    UPDATE Trades
    SET trade_status = '0'
    WHERE user_id = %s AND setting_id = %s AND market_id = %s
  '''
  payload = (user_id, setting_id, market_id)
  cursor.execute(query, payload)
  conn.commit()

# 매도 라인 체크
def sell(price_data, settings_data, trade_data) :
  # 구매 가격과 현재 가격을 비교하면서 체크, 이익 설정 %에 도달하면 매도
  # 구매 목록을 가져와서 차례로 확인
  for trade in trade_data :
    if trade['trade_status'] == '0' :
      continue
    
    
    market_id = trade['market_id']
    user_id = trade['user_id']
    setting_id = trade['setting_id']
    # 거래 가격
    # trade_price = float(trade['trade_price'])
    
    # print(trade_price)
    market_data = get_market_name(trade['market_id'])
    market_code = market_data['market_code']
    market_code_split = market_code.split('-')[1]
    # print(market_code)
    key = get_user_key(user_id)
    asset = get_user_asset(market_code_split, key)
    if isinstance(get_user_trade_price(market_code_split, key), list):
      print('매수 체결 미완료')
      continue
    trade_price = float(get_user_trade_price(market_code_split, key))
    
    # 현재 가격
    data = price_data.reindex(columns = [market_code])
    data = data.iloc[-1].to_json(orient='split')
    data = json.loads(data)['data']
    # print(data)
    c_price = float(data[0].split(',')[0][1:])
    print(c_price)
    print(trade_price)
    
    # % 구하기
    result = round((c_price - trade_price) / c_price * 100, 2)
    print(result)
    
    # trade 테이블에서 예약번호(setting_name)를 가지고오고 그 예약번호의 매도 이익률(setting_benefit)을 가져온다
    
    setting_data = get_setting_benefit(user_id, setting_id)
    # 받아오는 데이터가 배열로 감싸져 있기 때문에 0번 인덱스의 setting_benefit을 가져옴
    # print(setting_data[0]['setting_benefit'])
    setting_benefit = setting_data[0]['setting_benefit']
    setting_loss = setting_data[0]['setting_loss']
    
    # 트레이드 0으로 바꿔주고
    # 팔기 전에 트레이드 1인것만 체크하는 코드
    
    if result >= float(setting_benefit):
      sell_order(market_code, asset, key)
      print('매도')
      set_trade_status(user_id, setting_id, market_id)
    elif result <= -float(setting_loss):
      sell_order(market_code, asset, key)
      print('손절')
      set_trade_status(user_id, setting_id, market_id)
    else :
      key = get_user_key(user_id)
      asset = get_user_asset(market_code_split, key)
      print('보유')

# 언채 함수
def chk_already_trade(user_id, market_id):
  date = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d')
  query = '''
    SELECT * 
    FROM Trades
    WHERE user_id = %s AND trade_created_at LIKE %s AND market_id = %s;
  '''
  payload = (user_id, date + "%", market_id)
  cursor.execute(query, payload)
  if len(cursor.fetchall()) < 1:
    return False
  else:
    return True
  
def set_trade_data(payload):
  now = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
  query = '''
    INSERT INTO Trades(
      user_id, 
      market_id, 
      setting_id,
      trade_price,
      trade_status,
      trade_created_at
    ) 
    VALUES(%s, %s, %s, %s, %s, %s);
  '''
  payload = (payload['user_id'], payload['market_id'], payload['setting_id'], payload['trade_price'], '1', now)
  cursor.execute(query, payload)
  conn.commit() 
      
def buy_order(market, price, key):
    query = {
      'market': market,
      'side': 'bid',
      'price': price,
      'ord_type': 'price',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': key['access_key'],
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }
    
    jwt_token = jwt.encode(payload, key['secret_key'])
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
    print(res.json())
    
def get_data_to_s3():
  bucket_name = 'ats-data-bucket'
  try:
    #current
    c_now = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d-%H:%M:%S')
    c_date = c_now[0:10]
    c_hour = c_now[0:13]
    c_file_name = c_date + '/' + c_hour + '.csv'
    c_resp = client.get_object(Bucket=bucket_name, Key=c_file_name)
    c_df = pd.read_csv(c_resp['Body'], sep=',')
    
    #before
    b_now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d-%H:%M:%S')
    b_date = b_now[0:10]
    b_hour = b_now[0:13]
    b_file_name = b_date + '/' + b_hour + '.csv'
    b_resp = client.get_object(Bucket=bucket_name, Key=b_file_name)
    b_df = pd.read_csv(b_resp['Body'], sep=',')
    
    data = b_df.append(c_df)
    return data
        
  except Exception as err:
    print(err)
    
def buy(price_data, reservation_data):
  for r in reservation_data:
    if r['setting_active'] == 'true':
      # 모니터링 하고 있는 컬럼 항목만 남기기
      market_list = []
      for market in r['setting_market_id'].split(','):
        market_list.append(market)
      data = price_data.reindex(columns = market_list)
      # 사용자가 모니터링하기 원하는 시간 간격 설정
      data = data.iloc[[-7 * int(r['setting_time']), -1]].to_json(orient='split')
      # 코인 상 데이터만 표시
      column = json.loads(data)['columns']
      data = json.loads(data)['data']
      for item in data[0]:
        idx = data[0].index(item)
        b_price = float(item.split(',')[0][1:])
        c_price = float(data[1][idx].split(',')[0][1:])
        result = round((c_price - b_price) / c_price * 100, 2)
        print(column[idx] + ' ' + str(result))
        if result > float(r['setting_percent']):
          # 하루에 한번만 구매 trade테이블에서 구매된 시간이 오늘과 일치한 코인이라면 구매하지 않음
          market = get_market_code(column[idx])
          if chk_already_trade(r['user_id'], market['market_id']):
            # 오늘 구매된 코인일 경우 패스
            continue
          
          # 잔액과 setting price와 비교해서 setting price가 더 적다면 구매하지 않음
          key = get_user_key(r['user_id'])
          asset = get_user_asset('KRW', key)
          if float(asset) < float(r['setting_price']):
            continue
          
          # 구매
          buy_order(column[idx], int(r['setting_price']), key)
          
          # trade table에 데이터 생성
          asset = get_user_asset(column[idx], key)
          payload = {
            'user_id': r['user_id'],
            'market_id': market['market_id'],
            'setting_id': r['setting_id'],
            'trade_price': r['setting_price'],
          }
          set_trade_data(payload)
    else:
      print('out')
      continue
  
def lambda_handler():
  price_data = get_data_to_s3()
  setting_data = get_setting_data()
  buy(price_data, setting_data)
  trade_data = get_trade_data()
  sell(price_data, setting_data, trade_data)
  
lambda_handler()