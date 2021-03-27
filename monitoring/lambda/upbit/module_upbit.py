# modules
import os
import jwt
import datetime
import uuid
import hashlib
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv
import time

# init
load_dotenv(verbose=True)
server_url = os.getenv('URL')

# market, key
def get_asset(payload):
  _payload = {
    'access_key': payload['access_key'],
    'nonce': str(uuid.uuid4()),
  }
  jwt_token = jwt.encode(_payload, payload['secret_key'])
  authorize_token = 'Bearer {}'.format(jwt_token)
  headers = {"Authorization": authorize_token}
  data = requests.get(server_url + "/v1/accounts", headers=headers).json()
  for item in data:
    if item.get('currency') == payload['market']:
      data = item.get('balance')
  return data

# market, key
def get_trade_price(payload):
  _payload = {
    'access_key': payload['access_key'],
    'nonce': str(uuid.uuid4()),
  }
  jwt_token = jwt.encode(_payload, payload['secret_key'])
  authorize_token = 'Bearer {}'.format(jwt_token)
  headers = {"Authorization": authorize_token}
  data = requests.get(server_url + "/v1/accounts", headers=headers).json()
  for item in data:
    if item.get('currency') == payload['market']:
      data = item.get('avg_buy_price')
  return data

# market, asset_data, key
def sell_order(payload):
  now = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d-%H:%M:%S')
  identifier = 'ask' + now + payload['user_id'] + payload['setting_id'] + market_code
  query = {
    'market': payload['market'],
    'side': 'ask',
    'volume': payload['asset_data'],
    'ord_type': 'market',
    'identifier': identifier
  }
  query_string = urlencode(query).encode()
  m = hashlib.sha512()
  m.update(query_string)
  query_hash = m.hexdigest()
  _payload = {
    'access_key': payload['access_key'],
    'nonce': str(uuid.uuid4()),
    'query_hash': query_hash,
    'query_hash_alg': 'SHA512',
  }
  jwt_token = jwt.encode(_payload, payload['secret_key'])
  authorize_token = 'Bearer {}'.format(jwt_token)
  headers = {"Authorization": authorize_token}
  res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
  return identifier
  
# market, price, key
def buy_order(payload):
  now = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%Y%m%d%H%M%S')
  identifier = 'bid' + now + str(payload['user_id']) + str(payload['setting_id']) + payload['market_code'].split('-')[1]
  query = {
    'market': payload['market_code'],
    'side': 'bid',
    'price': payload['setting_price'],
    'ord_type': 'price',
    'identifier': identifier
  }
  query_string = urlencode(query).encode()
  m = hashlib.sha512()
  m.update(query_string)
  query_hash = m.hexdigest()
  _payload = {
    'access_key': payload['access_key'],
    'nonce': str(uuid.uuid4()),
    'query_hash': query_hash,
    'query_hash_alg': 'SHA512',
  }
  jwt_token = jwt.encode(_payload, payload['secret_key'])
  authorize_token = 'Bearer {}'.format(jwt_token)
  headers = {"Authorization": authorize_token}
  res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
  print(res.json())
  start_time = time.time()
  while True:
    response = getTradeData(identifier, payload)
    if(len(response['trades']) > 0):
      break
    time.sleep(0.1)
  print("--- %s seconds ---" % (time.time() - start_time))
  return response
  
def getTradeData(identifier, payload):
  query = {
    'identifier': identifier,
  }
  query_string = urlencode(query).encode()
  
  m = hashlib.sha512()
  m.update(query_string)
  query_hash = m.hexdigest()
  
  _payload = {
    'access_key': payload['access_key'],
    'nonce': str(uuid.uuid4()),
    'query_hash': query_hash,
    'query_hash_alg': 'SHA512',
  }
  
  jwt_token = jwt.encode(_payload, payload['secret_key'])
  authorize_token = 'Bearer {}'.format(jwt_token)
  headers = {"Authorization": authorize_token}
  
  res = requests.get(server_url + "/v1/order", params=query, headers=headers)
  
  return res.json()