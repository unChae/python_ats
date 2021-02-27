import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

# call .env
from dotenv import load_dotenv

load_dotenv(verbose=True)

access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
server_url = os.getenv('URL')

#bid 매수 ask 매도
query = {
    'market': 'KRW-BTT',
    'side': 'bid',
    'volume': '1',
    'price': '5000.0',
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

print(res.json())