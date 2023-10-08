import os
from typing import Any, List, Mapping, Optional, Dict

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from .model.http_alles_api_model import AllesMinimaxAPILLMModel, AllesChatGPTAPILLMModel, AllesGPT4APILLMModel, AllesPalmAPILLMModel, AllesClaudeAPILLMModel, AllesWenxinAPILLMModel, AllesSparkAPILLMModel, AllesBaiduTranslateAPILLMModel
from .model.http_puyu_api_model import PuyuAPILLMModel


class AllesChatLLM(LLM):
    model: str = None
    """Model name to use."""
    model_kwargs: Dict[str, Any] = None
    """Holds any model parameters valid for `create` call not explicitly specified."""
    temperature: float = None
    """What sampling temperature to use."""
    max_tokens: Optional[int] = None
    """Maximum number of tokens to generate."""

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        messages: Optional[List[dict]] = None,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if self.model.startswith("alles"):
            api_key = os.environ["ALLES_API_TOKEN"]
        elif self.model.startswith("puyu"):
            api_key = os.environ["PUYU_API_TOKEN"]
        
        params = {
            "api_key": api_key,
        }
        if self.model == "alles-minimax":
            model = AllesMinimaxAPILLMModel(**params)
        elif self.model == "alles-chatgpt":
            model = AllesChatGPTAPILLMModel(**params)
        elif self.model == "alles-gpt4":
            model = AllesGPT4APILLMModel(**params)
        elif self.model == "alles-palm":
            model = AllesPalmAPILLMModel(**params)
        elif self.model == "alles-claude":
            model = AllesClaudeAPILLMModel(**params)
        elif self.model == "alles-wenxin":
            model = AllesWenxinAPILLMModel(**params)
        elif self.model == "alles-spark":
            model = AllesSparkAPILLMModel(**params)
        elif self.model == "puyu":
            model = PuyuAPILLMModel(**params)
        else:
            raise NotImplementedError()

        response = model.response(
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