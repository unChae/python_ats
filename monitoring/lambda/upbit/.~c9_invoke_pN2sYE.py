# modules
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv

# init
load_dotenv(verbose=True)
server_url = os.getenv('URL')

def get_asset(market, key):
  payload = {
    'access_key': key['access_key'],
    'nonce': str(uuid.uuid4()),
  }
  jwt_token = jwt.encode(payload, key['secret_key'])
  authorize_token = 'Bearer {}'.format(jwt_token)
  headers = {"Authorization": authorize_token}
  data = requests.get(server_url + "/v1/accounts", headers=headers).json()
  for item in data:
    if item.get('currency') == market:
      data = item.get('balance')
  return data
  
def get_user_trade_price(market, key):
  payload = {
    'access_key': key['access_key'],
    'nonce': str(uuid.uuid4()),
  }
  jwt_token = jwt.encode(payload, key['secret_key'])
  authorize_token = 'Bearer {}'.format(jwt_token)
  headers = {"Authorization": authorize_token}
  data = requests.get(server_url + "/v1/accounts", headers=headers).json()
  for item in data:
    if item.get('currency') == market:
      data = item.get('avg_buy_price')
  print('----')
  print(market)
  print(data)
  print('----')
  return data
  
def sell_order(market, asset_data, key):
  query = {
    'market': market,
    'side': 'ask',
    'volume': asset_data,
    'ord_type': 'market',
  }
  query_string = urlencode(query).encode()

  m = hashlib.sha512()
  m.update(query_string)
  query_hash = m.hexdigest()

  payload = {
    'access_key': key['access_key'],
    'nonce': str(uuid.uuid4()),
    'query_hash': query_hash,
    'query_hash_alg': 'SHA512',
  }
  
  jwt_token = jwt.encode(payload, key['secret_key'])
  authorize_token = 'Bearer {}'.format(jwt_token)
  headers = {"Authorization": authorize_token}
  res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
  print(res.json())
  
def buy_order(market, price, key):
    query = {
      'market': market,
      'side': 'bid',
      'price': price,
      'ord_type': 'price',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': key['access_key'],
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }
    
    jwt_token = jwt.encode(payload, key['secret_key'])
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
    print(res.json())