import os
from typing import Any, List, Mapping, Optional, Dict
from pydantic import BaseModel
from .model.http_alles_api_model import (
    AllesMinimaxAPILLMModel,
    AllesChatGPTAPILLMModel,
    AllesGPT4APILLMModel,
    AllesPalmAPILLMModel,
    AllesClaudeAPILLMModel,
    AllesWenxinAPILLMModel,
    AllesSparkAPILLMModel,
    AllesBaiduTranslateAPILLMModel,
)
from .model.http_puyu_api_model import PuyuAPILLMModel
from .model.http_tigerbot_api_model import TigerbotAPILLMModel
from .model.http_mita_api_model import MitaAPILLMModel
from .model.http_jieyue_api_model import JieyueAPILLMModel
from .model.http_wuya_api_model import WuyaAPILLMModel
from .model.http_soul_api_model import SoulAPILLMModel


class AllesChatLLM(BaseModel):
    model: str = None
    """Model name to use."""
    model_kwargs: Dict[str, Any] = None
    """Holds any model parameters valid for `create` call not explicitly specified."""
    temperature: float = None
    """What sampling temperature to use."""
    max_tokens: Optional[int] = None
    """Maximum number of tokens to generate."""

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    @property
    def _llm_type(self) -> str:
        return "custom"

    async def __call__(
        self,
        prompt: str,
        messages: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> str:
        if self.model.startswith("alles"):
            api_key = os.environ["ALLES_API_TOKEN"]
        elif self.model.startswith("puyu"):
            api_key = os.environ["PUYU_API_TOKEN"]
        elif self.model.lower().startswith("tigerbot"):
            api_key = os.environ["TIGERBOT_API_TOKEN"]
        elif self.model.lower().startswith("mita"):
            api_key = os.environ["MITA_API_TOKEN"]
        elif self.model.lower().startswith("jieyue"):
            api_key = os.environ["JIEYUE_API_TOKEN"]

        params = {
            "api_key": api_key,
        }
        if self.model.lower() == "alles-minimax":
            model = AllesMinimaxAPILLMModel(**params)
        elif self.model.lower() == "alles-chatgpt":
            model = AllesChatGPTAPILLMModel(**params)
        elif self.model.lower() == "alles-gpt4":
            model = AllesGPT4APILLMModel(**params)
        elif self.model.lower() == "alles-palm":
            model = AllesPalmAPILLMModel(**params)
        elif self.model.lower() == "alles-claude":
            model = AllesClaudeAPILLMModel(**params)
        elif self.model.lower() == "alles-wenxin":
            model = AllesWenxinAPILLMModel(**params)
        elif self.model.lower() == "alles-spark":
            model = AllesSparkAPILLMModel(**params)
        elif self.model.lower() == "puyu":
            model = PuyuAPILLMModel(**params)
        elif self.model.lower() == "tigerbot":
            model = TigerbotAPILLMModel(**params)
        elif self.model.lower() == "mita":
            model = MitaAPILLMModel(**params)
        elif self.model.lower() == "jieyue":
            model = JieyueAPILLMModel(**params)
        elif self.model.lower() == "wuya":
            model = WuyaAPILLMModel(**params)
        elif self.model.lower() == "soul":
            model = SoulAPILLMModel(**params)
        else:
            raise NotImplementedError()

        response = await model.response(
            prompt=prompt,
            messages=messages,
            **{
                **self.model_kwargs,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                **kwargs,
            },
        )
        return response["generated_text"]

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model_name": self.model}
