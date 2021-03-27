import json
from sys import path
from time import sleep
from requests import request
import pandas as pd
import os
import datetime

path.append("/root/ats/flask/DB")
from market_query import get_marketCode as coins

url = "https://api.upbit.com/v1/candles/days?market="
api_request_cnt = 1
payload = []

def create_to_CSV(payload):
    csv_path = '/root/ats/monitoring/csvs/' + "a.csv"
    column = []  # csv의 컬럼 값 
    data = {}    # csv의 행 값
    
    # pandas DataFrame에 넣기 위한 row, colunm 작성
    for item in payload :
        # print(item)
        column.append(item['coin_name'])
        data[item['coin_name']] = [item['trade_price']]
    
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    
    if os.path.isfile(csv_path) :
        # 기존에 파일이 있으면 행만 추가(header=False)
        df = pd.DataFrame(data, index=[now])
        df.to_csv(csv_path, mode='a', header=False)
    else :
        # 다음날이 되어서 파일이 없다면 생성
        df = pd.DataFrame(data, index=[now])
        df.to_csv(csv_path)

for index, coin in enumerate(coins(), start = 1):
    
    print(f"\n[{index}] {coin['market_code']}") 
    
    coin_by_date = request(
            "GET", 
            url + coin['market_code'], 
            params={"count": str(1)}
        )
        
    data = coin_by_date.json()
    # print(data)
    
    payload.append({
        "coin_name": data[0]['market_code'],
        "date_time": data[0]['candle_date_time_utc'],
        "trade_price": data[0]['trade_price']
    })
    
    # for item in coin_by_date.json():
    #     # print(f"{item['candle_date_time_utc'][0:10]} -> {item['trade_price']}")
    #     print(item)
    #     payload.append({
    #         "coin_name": coin['market_code'],
    #         "date_time": item['candle_date_time_utc'][0:10],
    #         "trade_price": item['trade_price']
    #     })
        
    if api_request_cnt % 10 == 0: sleep(1)
    api_request_cnt += 1
    
    print(payload)
    

# create_to_CSV(payload)


            

# csv file에 알맞은 값을 insert 하기만 하면 됨
