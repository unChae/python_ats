import json
from sys import path
from time import sleep
from requests import request
import pandas as pd
import os
import datetime
import csv

path.append("/root/ats/flask/DB")
from market_query import get_marketCode as coins

url = "https://api.upbit.com/v1/candles/days?market="
api_request_cnt = 1
payload = []

for index, coin in enumerate(coins(), start = 1):
    coin_by_date = request(
            "GET", 
            url + coin['market_code'], 
            params={"count": str(1)}
        )
          
    for item in coin_by_date.json():
        payload.append({
            "coin_name": coin['market_code'],
            "date_time": item['candle_date_time_utc'][0:10],
            "trade_price": item['trade_price']
        })
        
    if api_request_cnt % 10 == 0: sleep(1)
    api_request_cnt += 1

어제의 코인별 데이터 
print(payload) 



# SCV 파일끝행 payload 추가 

test = pd.read_csv("./test.csv")
print(test)




# SCV 파일 첫행 삭제 


#열 인덱스 생성
df = pd.DataFrame(friends, columns = ['name','age', 'job']) 

df = df.drop(df.index[[0,2]])



