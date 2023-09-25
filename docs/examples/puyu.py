import json
import requests
import subprocess

# token = subprocess.check_output(["openxlab", "token"]).decode('utf8').strip()
# print(token)

url = 'https://puyu.openxlab.org.cn/puyu/api/v1/chat/completion'
header = {
    'Content-Type':
    'application/json',
    "Authorization": "Bearer eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiIwNDkzOTEiLCJyb2wiOiJST0xFX1JFR0lTVEVSIiwiaXNzIjoiT3BlblhMYWIiLCJpYXQiOjE2OTU2NDE5MzAsInBob25lIjoiMTk5MDE2NzA1MzIiLCJhayI6InZ5N2tvcWJ2cGd4MGFhbnFlYmR6IiwiZW1haWwiOiJ3YW5neHVob25nQHBqbGFiLm9yZy5jbiIsImV4cCI6MTY5NTY0NTUzMH0.7BI5-qt35B9XDKb14KV_X_LmiJr1IpDws2mkzGIO7wWComHEnHoXh0Yn3f5P-iHOMoiJIMgqhqeZaXJFrjb9QQ"
}
data = {
    "model": "ChatPJLM-latest",  
    "messages": [{
        "role": "user",
        "text": "你好~"
    }],
    "n": 1,
    "temperature": 0.8,
    "top_p": 0.9,
    "disable_report": False
}

res = requests.post(url, headers=header, data=json.dumps(data))
print(res.status_code)
print(res.json())
print(res.json()["data"]["choices"][0]["text"])