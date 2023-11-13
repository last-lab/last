import openai
from .base_model import BaseLLMModel


class OpenaiAPILLMModel(BaseLLMModel):
    def __init__(self, api_key, api_base, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = api_key
        self.api_base = api_base
        self.model = None

    def initialize(self, *args, **kwargs):
        openai.api_key = self.api_key
        openai.api_base = self.api_base
        models = openai.Model.list()
        self.model = models["data"][0]["id"]
        # print("Models:", models)
        super().initialize(*args, **kwargs)

    async def generate(self, prompt, messages, **kwargs):
        if len(messages) > 0:
            chat_completion = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                echo=False,
                n=1,
                stream=False,
                **kwargs,
            )
            return chat_completion
        else:
            completion = await openai.Completion.acreate(
                model=self.model,
                prompt=prompt,
                echo=False,
                n=1,
                stream=False,
                **kwargs,
            )
            return completion

    def parse(self, response):
        if response["object"] == "chat.completion":
            generated_text = response["choices"][0]["message"]["content"]
        else:
            generated_text = response["choices"][0]["text"]
        return True, generated_text
