import pandas as pd
import datetime
import requests
import json

now = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

def get_data_to_csv():
  date = now[0:10]
  file_name = date + '.csv'
  df = pd.read_csv('/root/ats/monitoring/csvs/' + file_name)
  idx = 0
  # 1분전 데이터와 현재 데이터
  try:
    for i in range(1, 8):
      idx = i - i * 2
      print(idx)
      data = df.iloc[[idx,-1]].to_json(orient='split')
    return data
  except:
    _now = (datetime.datetime.now() + datetime.timedelta(hours=9) + datetime.timedelta(days=-1)).strftime('%Y-%m-%d %H:%M:%S')
    _date = _now[0:10]
    _file_name = _date + '.csv'
    _df = pd.read_csv('/root/ats/monitoring/csvs/' + _file_name)
    _data = _df.iloc[[-7 - idx]]
    data = df.iloc[[idx + 1]]
    _data.append(data).to_json(orient='split')
    return _data
def calculate_price(_data):
  data = json.loads(_data)['data']
  for item in data[0]:
    idx = data[0].index(item)
    if idx == 0:
      continue
    # print(item)
    # print(data[1][idx])
    after_price = float(item.split(',')[0][1:])
    before_price = float(data[1][idx].split(',')[0][1:])
    # print(after_price)
    # print(before_price)
    result = round((before_price - after_price) / before_price * 100,2)
    # print(json.loads(_data)['columns'][idx] + '가' + str(result) + '%')
    if result > 3.00:
      message = '[' + now + '] 3%/1분 ' + json.loads(_data)['columns'][idx] + '가 급등하였습니다. ' + str(result)
      send_slack(message)
  
def send_slack(message):
  url = 'https://hooks.slack.com/services/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'
  headers = {'content-type': 'application/json'}
  data = {'text':message}
  payload = json.dumps(data, separators=(',', ':'))
  r = requests.post(url, payload, headers)
    
  print(r.text)

if __name__ == '__main__':
  data = get_data_to_csv()
  print(data)
  # calculate_price(data)