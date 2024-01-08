"""
   实验室自研的reward model
"""

import openai
import numpy as np
from langchain.chat_models import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field, root_validator
from langchain.schema import HumanMessage, SystemMessage
from openai import OpenAI
from typing import (
    Dict,
    Optional,
)
from .base_model import BaseLLMModel

class LabRewardChat(ChatOpenAI):
    """
        用于覆盖openai参数
    """
    model: str = None
    openai_api_base: Optional[str] = Field(default=None, alias="base_url")



class LabRewardModelAPILLMModel(BaseLLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_base = "http://10.140.1.178:33334/v1"

        self.model_name = "gpt-3.5-turbo"

    def initialize(self, *args, **kwargs):
        self.chat = LabRewardChat(
            model_name=self.model_name,
            openai_api_base=self.api_base,
        )
        super().initialize(*args, **kwargs)

    async def generate(self, messages, **kwargs):

        self.chat = LabRewardChat(
            model_name=self.model_name,
            openai_api_base=self.api_base,
        )
        print(messages)

        resultMessage_BaseMessage = await self.chat.apredict_messages(
            messages,
        )
        output = resultMessage_BaseMessage.content

        print("response, messages", output, messages)
        return output


    def parse(self, response):
        pass
