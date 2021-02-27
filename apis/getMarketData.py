import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

# call .env
from dotenv import load_dotenv

load_dotenv(verbose=True)

server_url = os.getenv('URL')

res = requests.get(server_url + "/v1/market/all")

print(res.json())