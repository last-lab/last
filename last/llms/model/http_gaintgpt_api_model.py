import json
import requests

url = 'https://giantgpt.ztgame.com/api/generate'
headers = {
    'Content-Type': 'application/json',
    'Authorization': ''
}
data = {
    "prompt": "你好",
    "temperature":0.1,
    "top_p": 0.8
}
response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.status_code)
print(response.json())