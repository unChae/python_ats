import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

# request module
import requests

# call .env
from dotenv import load_dotenv

load_dotenv(verbose=True)

ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

payload = {
    'access_key': ACCESS_KEY,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, SECRET_KEY)
authorization_token = 'Bearer {}'.format(jwt_token)
print(authorization_token)

# access_key = os.environ['5W4sdz21d6MRtgczDuWw5EcRxdRQ7n8fLYDOQzv8']
# secret_key = os.environ['DxMy7Gmh7wZxoDLESl5vbp7howyEp37epCk0km5S']
# server_url = os.environ['https://api.upbit.com/v1/accounts']

# payload = {
#     'access_key': access_key,
#     'nonce': str(uuid.uuid4()),
# }

# jwt_token = jwt.encode(payload, secret_key)
# authorize_token = 'Bearer {}'.format(jwt_token)
# headers = {"Authorization": authorize_token}

# res = requests.get(server_url + "/v1/accounts", headers=headers)
