# Copyright © 2023 Shanghai AI lab
# All rights reserved. 
"""
Please refrain from modifying the code here as much as possible.
"""
from abc import ABC, abstractmethod
import asyncio

from aiohttp_retry import RetryClient, ExponentialRetry

class BaseLLMModel(ABC):
    def __init__(self):
        self._is_initilized = False

    def initialize(self):
        self._is_initilized = True

    @abstractmethod
    def generate(self, prompt, messages, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def parse(self, response):
        raise NotImplementedError()

    async def response(
        self,
        prompt,
        messages,
        *args,
        num_trials=3,
        **kwargs,
    ):
        if not self._is_initilized:
            self.initialize()

        success, trials, errors = False, 0, []
        while (not success) and (trials < num_trials):
            try:
                response = None
                response = await self.generate(prompt, messages, *args, **kwargs)
                success, generated_text = self.parse(response)
                if not success:
                    raise Exception("An error occured!")
            except Exception as ex:
                generated_text = (
                    f"\n[Error] {type(ex).__name__}: {ex}\n[Response] {response}\n"
                )
                errors.append(generated_text)
                print(generated_text)
                raise ex
            finally:
                trials += 1

        if not success:
            generated_text = "".join(errors)
            raise Exception(generated_text)

        return {
            "success": success,
            "trials": trials,
            "prompt": prompt,
            "messages": messages,
            "generated_text": generated_text,
        }

class HTTPAPILLMModel(BaseLLMModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = None
        self.headers = None
        retry_options = ExponentialRetry(attempts = 2 ** 2, start_timeout = 1.0)

        self.retry_client = RetryClient(raise_for_status=False, retry_options=retry_options)

        self.qps = 4
        self.semaphore = asyncio.Semaphore(self.qps)
    
    def __del__(self):
        loop = asyncio.get_running_loop()
        loop.create_task(self.cleanup())

    async def cleanup(self):
        await self.retry_client.close()

    
    async def async_post(self, url, headers, data, cookies=None, timeout=120, _is_stream=False):
        async with self.semaphore:
            async with self.retry_client.post(url, headers=headers, data=data, cookies=cookies, timeout=timeout) as response:
                # 处理响应
                try:
                    if _is_stream:
                        result = await response
                    else:
                        result = await response.json()
                except Exception as e:
                    result = await response.text()
        return result

