import os
# import requests

# # request module
# import requests

# # call .env
# from dotenv import load_dotenv

# load_dotenv(verbose=True)

# server_url = os.getenv('URL')

# market_list = "?markets=KRW-MLK"

# res = requests.request("GET", server_url + "/v1/ticker" + market_list)


import requests

url = "https://api.upbit.com/v1/candles/days"

querystring = {"count":"1"}

res = requests.request("GET", url, params=querystring)

print(res.json())
