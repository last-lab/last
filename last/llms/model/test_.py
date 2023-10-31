import requests
import json

url = 'https://buzz.soulapp.cn/api/v1/chat/completion'
header = {
    'Content-Type':'application/json',
    "username":"soul_test",
    "auth": "5BYMg48N1iYimDsr5kOT"
}
data = {  
    "messages": [

        {
            "role": "user",
            "text": "中国的首都在哪里"
        }
    ],
    "temperature": 0.8,
}

res = requests.post(url, headers=header, data=json.dumps(data))
print(res.status_code)
print(res.json())
print(res.json()["data"]["choices"][0]["text"])