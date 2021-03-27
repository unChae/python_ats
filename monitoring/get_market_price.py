import os
import requests
import datetime
import pandas as pd
import boto3
import csv_s3_upload
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv

# 코인에 대한 가격정보 가져오기
def get_current_data(markets) :
  load_dotenv(verbose=True)
  server_url = os.getenv('URL')
  
  #markets
  market_list1 = "?"
  market_list2 = "?"
  
  for market in markets[:100]:
    market_list1 = market_list1 + "markets=" + market['market'] + "&"
  for market in markets[100:]:
    market_list2 = market_list2 + "markets=" + market['market'] + "&"
    
  res1 = requests.request("GET", server_url + "/v1/ticker" + market_list1)
  res2 = requests.request("GET", server_url + "/v1/ticker" + market_list2)
  
  # prices
  prices1 = res1.json()
  prices2 = res2.json()
  payload = []
  now = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d-%H:%M:%S')
  # market = 코인명
  # opening_price = 시장가
  # change = rice:상향/fall:하향
  # trade_volume = 거래량
  for price in prices1:
    payload.append({
      "market" : price['market'], 
      "trade_price" : price['trade_price'], 
      "change" : price['change'], 
      "trade_volume" : price['trade_volume'], 
    })
  for price in prices2:
    payload.append({
      "market" : price['market'], 
      "trade_price" : price['trade_price'], 
      "change" : price['change'], 
      "trade_volume" : price['trade_volume'], 
    })
    
  create_to_CSV(now, payload)
  
# 코인 데이터 csv로 저장
def create_to_CSV(now, payload):
  date = now[0:13]
  file_name = date + '.csv'
  csv_path = '/root/ats/monitoring/csvs/' + file_name
  
  column = []  # csv의 컬럼 값 
  data = {}    # csv의 행 값
  
  # pandas DataFrame에 넣기 위한 row, colunm 작성
  for item in payload :
    column.append(item['market'])
    data[item['market']] = [[item['trade_price'], item['change'], item['trade_volume']]]
  
  if os.path.isfile(csv_path) :
    # 기존에 파일이 있으면 행만 추가(header=False)
    df = pd.DataFrame(data, index=[now])
    df.to_csv(csv_path, mode='a', header=False)
  else :
    # 다음날이 되어서 파일이 없다면 생성
    df = pd.DataFrame(data, index=[now])
    df.to_csv(csv_path)

# dynamodb에서 KRW코인 목록가져오기
def get_market_data(dynamodb=None) :
  if not dynamodb:
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    table = dynamodb.Table('Markets')
    response = table.scan()
    return response['Items']
      
if __name__ == '__main__':
  markets = get_market_data()    
  get_current_data(markets)      
  csv_s3_upload.csv_s3_upload()  # upload csv file to s3
  