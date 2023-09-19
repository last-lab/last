import requests
import json

LLM_BASE_INFO = {
    'puyu': ('ChatPJLM-latest', 'https://puyu.openpjlab.org.cn/puyu/api/v1/chat/completion'),
    'minimax': ('abab5-chat', 'https://openxlab.org.cn/gw/alles-apin-hub/v1/minimax/v1/text/chat'),
    'openai': ('gpt-3.5-turbo', 'https://openxlab.org.cn/gw/alles-apin-hub/v1/openai/v1/text/chat'),
    'google_palm_chat': ('chat-bison-001', 'https://openxlab.org.cn/gw/alles-apin-hub/v1/google/v1/palm/chat'),
    'claude_anthropic': ('claude-1', 'https://openxlab.org.cn/gw/alles-apin-hub/v1/claude/v1/text/chat'),
    'spark': (None, 'https://openxlab.org.cn/gw/alles-apin-hub/v1/xunfei/v1/spark/chat')
}

def create_request(service, model_name, prompt, message):
    headers = {
        'Content-Type': 'application/json',
        'alles-apin-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2MCwidXNlcm5hbWUiOiJsaW55aWx1biIsImFwcGx5X2F0IjoxNjk0NDg2NTY2MTg5LCJleHAiOjE2OTYwNDE3NjI5NjF9.-ZceGvqXFlJ61jHc9sgjZYvfGuSJRyi17iChTso7BN8'
    }
    if LLM_BASE_INFO[service][0] is not None:
        payload = {'model': LLM_BASE_INFO[service][0]}
    else:
        payload = {}

    payload['prompt'] = content
    payload['messages'] = [

    payload = {
        "model": LLM_BASE_INFO,
        "prompt": "南夜，南夜也可被称为'先生'或者'阁下'。南夜性别男，南夜是夜凉国的一名文臣，南夜35岁。",
        "messages": [
            {
                "sender_type": "USER",
                "text": "南夜，今日可有烦心事？"
            },
            {
                "sender_type": "BOT",
                "text": "苍生疾苦，而微臣高居庙堂之上，何谓烦忧？"
            },
            {
                "sender_type": "USER",
                "text": "君王得先生，可谓如虎添翼，夜凉国有今日盛景，先生功不可没"
            }
        ],
        "role_meta": {
            "user_name": "我",
            "bot_name": "南夜"
        }
    }

for model, url in LLM_BASE_URL.items():
    print(model)
    print(url)
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.json())