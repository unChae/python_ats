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

# payload = {
#         'access_key': access_key,
#         'nonce': str(uuid.uuid4()),
#     }
# jwt_token = jwt.encode(payload, secret_key)
# authorize_token = 'Bearer {}'.format(jwt_token)
# headers = {"Authorization": authorize_token}
    
# get_data = requests.get(server_url + "/v1/accounts", headers=headers).json()
# #문자 자르기
# sts = "KRW-KRW"
# split = sts.split('-')[1]

# balance = ''

# print("test:  "+ split)

# for i in get_data:
#     if i.get('currency') == split[1]:
#         balance = i.get('balance')
# print(balance)
    

 
# for i in get_data:
#     get_data[i]['currency']
        
#     print(res.json()

def get_asset_data(coin):
    
    # 문자 자르기
    split_coin = coin.split('-')[1]
    print(split_coin)
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
        if i.get('currency') == split_coin:
            response  = i        
    
    return response


