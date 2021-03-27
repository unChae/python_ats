import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

# call .env
from dotenv import load_dotenv

sys.path.append("/root/ats")
from create_log import createLogs
#response
sys.path.append("/root/ats/flask")
from make_response import cus_respones


load_dotenv(verbose=True)

access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
server_url = os.getenv('URL')

#bid 매수 ask 매도
# query = {
#     'market': 'KRW-BTT',
#     'side': 'bid',
#     'volume': '1',
#     'price': '5000.0',
#     'ord_type': 'price',
# }
# query_string = urlencode(query).encode()

# m = hashlib.sha512()
# m.update(query_string)
# query_hash = m.hexdigest()

# payload = {
#     'access_key': access_key,
#     'nonce': str(uuid.uuid4()),
#     'query_hash': query_hash,
#     'query_hash_alg': 'SHA512',
# }

# jwt_token = jwt.encode(payload, secret_key)
# authorize_token = 'Bearer {}'.format(jwt_token)
# headers = {"Authorization": authorize_token}

# res = requests.post(server_url + "/v1/orders", params=query, headers=headers)

# print(res.json())

#매수
def buy_order(coin, price):
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
    
    createLogs(1, order+" by "+coin)
    return cus_respones(200, "ok", res)

#매도
def sell_order(coin, volume):
    query = {
        'market': coin,
        'side': 'ask',
        'volume': volume,
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
    
    createLogs(1, order+" by "+coin)
    return cus_respones(200, "ok", res)