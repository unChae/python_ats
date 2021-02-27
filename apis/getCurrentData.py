import os
import requests

# request module
import requests

# call .env
from dotenv import load_dotenv

load_dotenv(verbose=True)

server_url = os.getenv('URL')

market_list = "?markets=KRW-BTC&markets=KRW-ETH"

res = requests.request("GET", server_url + "/v1/ticker" + market_list)

print(res.json())