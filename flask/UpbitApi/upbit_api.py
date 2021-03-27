import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import json
import requests

# call .env
from dotenv import load_dotenv

load_dotenv(verbose=True)

access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
server_url = os.getenv('URL')

#코인 시세 조회
def current_data(market_code):
    load_dotenv(verbose=True)

    server_url = os.getenv('URL')
    market_list = "?markets=" + market_code
    
    res = requests.request("GET", server_url + "/v1/ticker" + market_list)
    response = res.json()[0].get('trade_price')
    return response

#자산 반환
def get_asset(market_code):
    
    #문자 자르기 EX) "KRW-BTC" = "BTC"
    split_market_code = market_code.split('-')[1]
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }
    
    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    
    get_data = requests.get(server_url + "/v1/accounts", headers=headers).json()

    #찾고자 하는 데이터가 있으면 response에 넣어주고 반환한다
    for i in get_data:
        if i.get('currency') == split_market_code:
            response  = i        
    
    return response

#매도
def sell_order(market_code):
    
    asset_data = get_asset(market_code)['balance']
    
    query = {
        'market': market_code,
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
    return res
#거래 내역

def get_order_list():
    
    query = {
    'state': 'done',
    }
    query_string = urlencode(query)
    
    uuids = [
        '9ca023a5-851b-4fec-9f0a-48cd83c2eaae',
        #...
    ]
    uuids_query_string = '&'.join(["uuids[]={}".format(uuid) for uuid in uuids])
    
    query['uuids[]'] = uuids
    query_string = "{0}&{1}".format(query_string, uuids_query_string).encode()
    
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
    
    res = requests.get(server_url + "/v1/orders", params=query, headers=headers)
    
    print(res.json())