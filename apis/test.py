import requests

url = "https://api.upbit.com/v1/candles/days?market=KRW-BTC"

querystring = {"count":"2"}
response = requests.request("GET", url, params=querystring)

print(response.text)

# 1. get coins 
# 2. get database 

# print(f"- Start update : {_domain}/{_property}")