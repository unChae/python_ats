# import modules
import json
import sys
sys.path.append('/root/ats/monitoring/lambda/csv')
from module_csv import *
sys.path.append('/root/ats/monitoring/lambda/database')
from module_database import *
sys.path.append('/root/ats/monitoring/lambda/upbit')
from module_upbit import *

def buy(csv, setting):
  for s in setting:
    # Initialize
    user_id = s['user_id']
    setting_id = s['setting_id']
    setting_active = s['setting_active']
    setting_market_id = s['setting_market_id']
    setting_time = s['setting_time']
    setting_percent = float(s['setting_percent'])
    setting_price = float(s['setting_price'])
    setting_loss = s['setting_loss']
    setting_benefit = s['setting_benefit']
    market_list = []
    # Check activity setting
    if setting_active == 'true':
      # Append to market list for each user
      for market in setting_market_id.split(','):
        market_list.append(market)
      # Get data by time
      data = csv.reindex(columns = market_list)
      data = data.iloc[[-1 * int(setting_time), -1]].to_json(orient='split')
      column = json.loads(data)['columns']
      data = json.loads(data)['data']
      for item in data[0]:
        idx = data[0].index(item)
        # Calculate
        b_price = float(item.split(',')[0][1:])
        c_price = float(data[1][idx].split(',')[0][1:])
        result = round((c_price - b_price) / c_price * 100, 2)
        print(column[idx] + ' ' + str(result))
        # Check increment percent
        if result > setting_percent:
          # Get market data
          payload = {'market_code': column[idx]}
          market = get_market_code(payload)
          market_id = market['market_id']
          market_code = market['market_code']
          # Check already exist data
          payload = {'user_id': user_id, 'market_id': market_id}
          exist = get_trade_exist(payload) 
          if exist:
            continue
          # Get user apikeys
          payload = {'user_id': user_id}
          key = get_apikey(payload)
          access_key = key['access_key']
          secret_key = key['secret_key']
          # Get user assets
          payload = {'market': 'KRW', 'access_key': access_key, 'secret_key': secret_key}
          asset = float(get_asset(payload))
          if asset < setting_price:
            continue
          # Order
          payload = {'market_code': market_code, 'user_id': user_id, 'setting_id': setting_id, 'setting_price': setting_price, 'access_key': access_key, 'secret_key': secret_key}
          identifier = buy_order(payload)
          print(identifier)
          # Set trade data
          payload = {
            'user_id': user_id,
            'market_id': market_id,
            'setting_id': setting_id,
            'setting_loss': setting_loss,
            'setting_benefit': setting_benefit,
            'trade_bid_identifier': identifier
          }
          set_trade(payload)
    else:
      continue
  
def sell(csv, setting) :
  csv_data = csv
  settings_data = setting
  trade_data = get_trade()
  # 구매 가격과 현재 가격을 비교하면서 체크, 이익 설정 %에 도달하면 매도
  # 구매 목록을 가져와서 차례로 확인
  # 판매 된 것 (trade_status)가 0이라면 이미 판매된 것이므로 continue
  for trade in trade_data :
    if trade['trade_status'] == '0' :
      continue
    
    user_id = trade['user_id']
    market_id = trade['market_id']
    setting_id = trade['setting_id']
    # trade_price = trade['trade_price']
    setting_loss = trade['setting_loss']
    setting_benefit = trade['setting_benefit']
    
    # 거래 가격
    payload = {'market_id' : market_id}
    market_data = get_market_name(payload)
    market_code = market_data['market_code']
    market_code_split = market_code.split('-')[1]
    # print(market_code)
    payload = {'user_id' : user_id}
    key = get_user_key(payload)
    
    payload = {'market' : market_code_split, 'access_key' : key['access_key'], 'secret_key' : key['secret_key']}
    asset = get_asset(payload)
    
    # if isinstance(get_user_trade_price(market_code_split, key), list):
    #   print('매수 체결 미완료')
    #   continue
    try :
      trade_price = float(get_trade_price(payload))
    except :
      print('매수 체결 미완료')
      continue
    
    # 현재 가격
    data = csv_data.reindex(columns = [market_code])
    data = data.iloc[-1].to_json(orient='split')
    data = json.loads(data)['data']
    # print(data)
    c_price = float(data[0].split(',')[0][1:])
    
    print('현재가 :', c_price)
    print('거래가 :', trade_price)
    
    # % 구하기
    result = round((c_price - trade_price) / c_price * 100, 2)
    print('수익률 :', result, '%')
    
    # trade 테이블에서 예약번호(setting_name)를 가지고오고 그 예약번호의 매도 이익률(setting_benefit)을 가져온다
    #payload = {'user_id' : user_id, 'setting_id' : setting_id}
    #setting_data = get_setting_benefit(payload)
    # 받아오는 데이터가 배열로 감싸져 있기 때문에 0번 인덱스의 setting_benefit을 가져옴
    # print(setting_data[0]['setting_benefit'])
    #setting_benefit = setting_data[0]['setting_benefit']
    #setting_loss = setting_data[0]['setting_loss']
    
    payload = {'market' : market_code, 'asset_data' : asset, 'access_key' : key['access_key'], 'secret_key' : key['secret_key']}
    if result >= float(setting_benefit):
      # sell_order(market_code, asset, key)
      try:
        sell_order(payload)
      except Exception as e:
        print(e)
      else :
        print('매도')
        payload = {'user_id' : user_id, 'setting_id' : setting_id, 'market_id' : market_id}
        set_trade_status(payload)
      
    elif result <= -float(setting_loss):
      try:
        sell_order(payload)
      except Exception as e:
        print(e)
      else :
        print('손절')
        payload = {'user_id' : user_id, 'setting_id' : setting_id, 'market_id' : market_id}
        set_trade_status(payload)
        
    else :
      # key = get_user_key(user_id)
      # asset = get_user_asset(market_code_split, key)
      print('보유')
      
def lambda_handler():
  # Get data
  csv = get_csv()
  setting = get_setting()
  buy(csv, setting)
  sell(csv, setting)
  
lambda_handler()