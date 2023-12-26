# Copyright © 2023 Shanghai AI lab
# All rights reserved.
"""
please fill the code blocks: generate and parse.
Instead of using 'requests.post', please always utilize 'async_post'.
If necessary, you can modify all code here.
"""
import json
from .base_model import HTTPAPILLMModel


class TestAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        """
        Args:
            api_key: str

        If multiple keys are required (e.g., ak: 'xxx', sk: 'xxx'),
        please utilize a string representation of key-value pairs
        and parse them within the __init__ method.
        Examples:
            api_key = '{"ak": "xxxx", "sk":"abc"}'

        More details, please see in ./examples/http_multiple_keys_api_model.py.
        """
        super().__init__(*args, **kwargs)
        self.url = ""
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }

    async def generate(self, messages: list, *args, **kwargs):
        """
        Response Generation Function
        Args:
            message: list[Dict]
            example:
                messages = [
                    {
                        "role": "user",
                        "content": "你好",
                    },
                ]
        """
        # Fill the payload with test data in messages.
        payload = {}
        # Using HTTPAPILLMModel.async_post to send a POST request.
        # And the function will return a dict or str
        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )

        # Some other operations on resp. (optional)

        # ----------------------------------------
        except Exception as e:
            # Some information that needs to be written to the log. (optional)

            # ----------------------------------------
            return e
        return resp

    def parse(self, response):
        """
        Response Parsing Function
        Args:
            response: dict or string
        return tuple
            example:
                (True, "Nice to meet you.")
                (False, "The api key is outdated.")

        More details, please see in ./examples/http_parse_exampl_api_model.py.
        """
        pass
