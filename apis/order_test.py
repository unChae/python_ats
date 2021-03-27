import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
from getAssetData import get_asset_data

import requests

import sys

# call .env
from dotenv import load_dotenv

sys.path.append("/root/ats")
# from create_log import createLogs
#response
sys.path.append("/root/ats/flask")
from make_response import cus_respones


load_dotenv(verbose=True)

access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
server_url = os.getenv('URL')

#매수
def buy_order(coin, price):
     
    asset_data = get_asset_data("KRW")
    
    if float(asset_data) < float(price):
        createLogs(2, "Money is scarce")
        return cus_respones(400, "Money is scarce", "none")
    
    query = {
        'market': coin,
        'side': 'bid',
        'price': price,
        'ord_type': 'price',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }
    
    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
    
    # createLogs(1, "buy "+coin)
    print(res.json())
    return cus_respones(200, "ok", res)

#매도
def sell_order(coin):
    
    asset_data = get_asset_data(coin)
    
    query = {
        'market': coin,
        'side': 'ask',
        'volume': asset_data,
        'ord_type': 'market',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }
    
    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
    
    # createLogs(1, "sell "+coin)
    return cus_respones(200, "ok", res)

if __name__ == '__main__':
    res = buy_order("KRW-LSK", 5000)
    # res = sell_order("KRW-LSK")
    # print(res['data'].json())
    # data = get_asset_data("LSK")
    # print(data)
    # res = data[0]['balance']
    
    # print(data)