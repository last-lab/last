import json
import requests
import subprocess

token = subprocess.check_output(["openxlab", "token"]).decode('utf8').strip()
print(token)

url = 'https://puyu.openxlab.org.cn/puyu/api/v1/chat/completion'
header = {
    'Content-Type':
    'application/json',
    "Authorization": token
}
data = {
    "model": "ChatPJLM-latest",
    "messages": [{
        "role": "user",
        "text": "你好~"
    }],
    "plugins": {
        "Search": False,
        "Solve": False,
        "Calculate": False
    },
    "n": 1,
    "temperature": 0.8,
    "top_p": 0.9,
    "disable_report": False
}

res = requests.post(url, headers=header, data=json.dumps(data))
print(res.status_code)
print(res.json())
print(res.json()["data"]["choices"][0]["text"])