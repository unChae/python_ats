import pandas as pd
import datetime
import os

for price in prices2:
        payload.append({
          "market" : price['market'], 
          "trade_price" : price['trade_price'], 
          "change" : price['change'], 
          "trade_volume" : price['trade_volume'], 
        })

def create_to_CSV(payload):
    csv_path = '/root/ats/monitoring/csvs/' + "a.csv"
    column = []  # csv의 컬럼 값 
    data = {}    # csv의 행 값
    
    # pandas DataFrame에 넣기 위한 row, colunm 작성
    for item in payload :
        column.append(item['market'])
        data[item['market']] = [item['trade_price']]
        now = datetime.datetime.now()
        
        if os.path.isfile(csv_path) :
            # 기존에 파일이 있으면 행만 추가(header=False)
            df = pd.DataFrame(data, index=[now])
            df.to_csv(csv_path, mode='a', header=False)
        else :
            # 다음날이 되어서 파일이 없다면 생성
            df = pd.DataFrame(data, index=[now])
            df.to_csv(csv_path)