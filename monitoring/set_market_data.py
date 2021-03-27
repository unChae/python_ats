import boto3
import os
import jwt
import uuid
import hashlib
import requests
import pymysql 
from urllib.parse import urlencode
from dotenv import load_dotenv

conn = pymysql.connect(host='atsdatabase.cx1qr2mihmj5.ap-northeast-2.rds.amazonaws.com', user='ats', password='rmatkddnjs4321!', db='ats', charset='utf8') 
cursor = conn.cursor() 
# 업비트에서 모든 코인 데이터를 가져오는 함수
def get_market_data() :
  load_dotenv(verbose=True)
  server_url = os.getenv('URL')
  res = requests.get(server_url + "/v1/market/all")
  return res.json()

# dynamodb에 KRW코인만 추출하여 저장
def put_market(market_json, dynamodb=None):
  if not dynamodb:
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')

    table = dynamodb.Table('Markets')
    
    for market in market_json:
      coin = market['market']
      kor_name = market['korean_name']
      eng_name = market['english_name']
      
      if coin[0:3] != 'KRW':
        continue
      
      # dynamodb에 insert
      import pymysql 
      sql = """
        INSERT INTO Markets (market_code, market_kor_name, market_eng_name)
        VALUES (%s, %s, %s);
      """
      cursor.execute(sql, (coin, kor_name, eng_name))
    conn.commit()
    return
    
if __name__ == '__main__':
  market_json = get_market_data()
  put_market(market_json)