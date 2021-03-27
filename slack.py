import requests
import json

url = 'https://hooks.slack.com/services/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'
headers = {'content-type': 'application/json'}
data = {'text':'hello'}
payload = json.dumps(data, separators=(',', ':'))
r = requests.post(url, payload, headers)

print(r.text)
