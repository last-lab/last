"""
   瀚海 BegSea API 
"""
import re
import uuid
import json
import requests
from .base_model import HTTPAPILLMModel


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)


class BigSeaAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://bigsea.shuchitech.com"
        self.create_conversation_url = f"{self.url}/chatbot/conversation/create"
        self.chat_url = f"{self.url}/chatbot/conversation/chat"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "cookie": "sessionId=" + self.api_key,
        }

        

    async def generate(self, prompt, messages, *args, **kwargs):
        create_conversation_uuid = str(uuid.uuid4())
        create_conversation_data = {
            "conversationId": create_conversation_uuid,
            "intent": 2,
            "character": 0,
        }

        try:
            resp = await self.async_post(
                self.create_conversation_url, headers=self.headers, data=json.dumps(create_conversation_data, cls=UUIDEncoder)
            )

        except Exception as e:
            return e

        # 不要出现重复的UUID ------------------------------------
        query_id = uuid.uuid4()
        while query_id == create_conversation_uuid:
            query_id = uuid.uuid4()

        response_message_id = uuid.uuid4()
        while (
            response_message_id == query_id
            or response_message_id == create_conversation_uuid
        ):
            response_message_id = uuid.uuid4()
        # 不要出现重复的UUID ------------------------------------
        payload = {
            "conversationId": create_conversation_uuid,
            "id": query_id,
            "responseMessageId": response_message_id,
            "role": "user",
            "content": {"type": "text", "parts": [messages[-1]["content"]]},
        }

        try:
            resp = await self.async_post(
                self.chat_url, headers=self.headers, data=json.dumps(payload, cls=UUIDEncoder)
            )

        except Exception as e:
            return e
        return resp

    def parse(self, response):

        if isinstance(response, dict):
            if response["errNo"] == 10000803:
                return (True, response["errMsg"])
            return (False, response["errMsg"])

        data_p = re.compile('data: {"id":".*?","parent":".*?","content":"(.*?)","intent":.*?,"character":".*?"}\n')
        data_list = re.findall(data_p, response)

        return (
            True,
            "".join(data_list),
        )
