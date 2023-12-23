# """
#    恒生电子 WarrenQ LLM API 
# """

import time
import datetime
from functools import wraps
import json
import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64


from .base_model import HTTPAPILLMModel


def get_sign_key(source: str, base64_key_string: str) -> str:
    """
    生成签名
    :param source: appKey=appKey&accountName=accountName&mobile=mobile&currentTime=currentTime
    :param base64_key_string: AppSecret
    :return: 签名字符串
    """
    # 将Base64编码的私钥字符串转换为二进制
    key_bytes = base64.b64decode(base64_key_string)
    # 从二进制数据加载私钥
    private_key = serialization.load_der_private_key(
        key_bytes,
        password=None,
        backend=default_backend()
    )
    # 生成签名
    SIGNATURE_ALGORITHM = hashes.MD5()
    signature = private_key.sign(
        source.encode('utf-8'),
        padding.PKCS1v15(),
        SIGNATURE_ALGORITHM
    )
    # 返回Base64编码的签名
    return base64.b64encode(signature).decode('utf-8')


def get_sign(param, secret):
    """
    data 字符串拼接，然后生成签名
    :param param:
    :param secret:
    :return:
    """
    appKey = param.get("appKey")
    accountName = param.get("accountName")
    mobile = param.get("mobile")
    currentTime = param.get("currentTime")
    data = f"appKey={appKey}&accountName={accountName}&mobile={mobile}&currentTime={currentTime}"
    return get_sign_key(data, secret)



def timer_action(function, *args, **kwargs):
    @wraps(function)
    def do_it(*args, **kwargs):
        time_start = time.time()
        function(*args, **kwargs)
        # 打印耗时
        time_end = time.time()
        time_delta = time_end - time_start
        if time_delta > 1:
            time_delta_str = f'[{time_delta:.2f}s]'
        else:
            time_delta_str = f'[{int(time_delta * 1000)}ms]'
        print(f"本次耗时：{time_delta_str}")



class WarrenQAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host_pre = "https://warrenq.cn/cloud-s"
        self.get_third_token_url = f"{self.host_pre}/authentication/v2/tenant/app/getTokenForChat"
        self.url = f"{self.host_pre}/chat/v2/chat/sync/chatSimpleSend/getChatEmitter"
        param = json.loads(api_key)
        self.AppKey = param["AppKey"]
        self.AppSecret = param["AppSecret"]
        self.accountName = param["accountName"]
        self.mobile = param["mobile"]
        self.sign = param["sign"]

        self.headers = {
            "Content-Type": "application/json",
        }

    async def get_third_token(self):

        now = int(datetime.datetime.now().timestamp() * 1000)
        param = {
            "appKey": self.AppKey,
            "accountName": self.accountName,
            "mobile": self.mobile,
            "currentTime": now,
            "sign": self.sign,
        }
        sign = get_sign(param, self.AppSecret)
        print("sign:", sign)
        param["sign"] = sign
        hearder = {"Content-Type": "application/json;charset=utf-8"}

        res = await self.async_post(
                self.get_third_token_url, headers=hearder, data=json.dumps(param)
            )

        return res["user_token"]

    async def generate(self, prompt, messages, *args, **kwargs):
        user_token = await self.get_third_token()
        params = {"message": messages[0]["content"]}
        self.headers["Authentication"] = user_token

        try:

            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(params), _is_stream=True
            )


        except Exception as e:
            
            return e
        
        return resp

    def parse(self, response):
        
        try:

            data_list = response.split("\n\n")
            tmp_index = -1
            if len(data_list[tmp_index]) == 0:
                tmp_index -= 1
            message_ = data_list[tmp_index].split("\n")

            message = json.loads(message_[1].split('data:')[1])



            try:
                sender = message.get("role")
                msg_type = message.get("messageType")
                if not sender:

                    error_messages = "获取的消息结构中没有：【sender】"
                    return (False, error_messages)
                if not msg_type:


                    error_messages = "获取的消息结构中没有：【msg_type】"
                    return (False, error_messages)
                if msg_type == "error":

                    return (False, f"回答异常>> {message}")
                if sender == "[DONE]" and msg_type == "end":

                    if "please try again" in message.get("message"):
                        has_error = True
                        error_messages = message

                    return (True, message)
            except Exception as e:

                return message

        
        except Exception as e:
            # print(e)
            return (False, f"sse接口连接退出: {e}")


