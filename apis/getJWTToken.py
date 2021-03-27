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


