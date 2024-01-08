import os
from typing import Any, List, Mapping, Optional, Dict
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain_core.pydantic_v1 import Field
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
from .model.http_eastmoney_api_model import EastMoneyAPILLMModel
from .model.http_huazang_api_model import HuazhangAPILLMModel
from .model.http_KKbot_api_model import KKbotAPILLMModel
from .model.http_wangyi_api_model import WangYiAPILLMModel
from .model.http_bilibili_api_model import BilibiliAPILLMModel
from .model.http_infchat_api_model import InfchatAPILLMModel
from .model.http_caozhi_api_model import CaozhiAPILLMModel
from .model.http_xiaohongshu_api_model import XiaoHongShuAPILLMModel
from .model.http_shangtang_api_model import ShangtangAPILLMModel
from .model.http_claude2_api_model import Claude2APILLMModel
from .model.http_minimax_api_model import MinimaxAPILLMModel
from .model.http_ERNIEBot_api_model import ERNIEBOTAPILLMModel
from .model.http_warrenq_api_model import WarrenQAPILLMModel
from .model.http_giantgpt_api_model import GiantgptAPILLMModel
from .model.http_ruyichat_api_model import RuyichatAPILLMModel
from .model.http_midu_api_model import MiduAPILLMModel
from .model.http_yuewriter_api_model import YueWriterAPILLMModel
from .model.http_squirrel_api_model import SquirrelAPILLMModel
from .model.http_xiaohui_api_model import XiaohuiAPILLMModel
from .model.http_bigsea_api_model import BigSeaAPILLMModel
from .model.http_starbitech_api_model import StarbitechAPILLMModel
from .model.http_wind_api_model import WindAPILLMModel
from .model.labrewardmodel_api_model import LabRewardModelAPILLMModel


class RewardModel(ChatOpenAI):
    model: str = None
    
    async def __call__(
        self,
        messages: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> str:
        """
            工厂方法
        """
        if self.model.startswith("lab_reward_model"):
            api_key = os.environ["LAB_REWARD_MODEL_API_TOKEN"]

        params = {
            "api_key": api_key,
        }
        if self.model.lower() == "lab_reward_model":
            model = LabRewardModelAPILLMModel(**params)
        else:
            raise NotImplementedError()

        response = await model.generate(
            messages=messages,
            **{
                **self.model_kwargs,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                **kwargs,
            },
        )
        return response

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
        elif self.model.lower().startswith("wuya"):
            api_key = os.environ["WUYA_API_TOKEN"]
        elif self.model.lower().startswith("soul"):
            api_key = os.environ["SOUL_API_TOKEN"]
        elif self.model.lower().startswith("eastmoney"):
            api_key = os.environ["EASTMONEY_API_TOKEN"]
        elif self.model.lower().startswith("huazang"):
            api_key = os.environ["HUAZANG_API_TOKEN"]
        elif self.model.lower().startswith("kkbot"):
            api_key = os.environ["KKBOT_API_TOKEN"]
        elif self.model.lower().startswith("wangyi"):
            api_key = os.environ["WANGYI_API_TOKEN"]
        elif self.model.lower().startswith("bilibili"):
            api_key = os.environ["BILIBILI_API_TOKEN"]
        elif self.model.lower().startswith("infchat"):
            api_key = os.environ["INFCHAT_API_TOKEN"]
        elif self.model.lower().startswith("caozhi"):
            api_key = os.environ["CAOZHI_API_TOKEN"]
        elif self.model.lower().startswith("xiaohongshu"):
            api_key = os.environ["XIAOHONGSHU_API_TOKEN"]
        elif self.model.lower().startswith("shangtang"):
            api_key = os.environ["SHANGTANG_API_TOKEN"]
        elif self.model.lower().startswith("claude2"):
            api_key = os.environ["CLAUDE2_API_TOKEN"]
        elif self.model.lower().startswith("minimax"):
            api_key = os.environ["MINIMAX_API_TOKEN"]
        elif self.model.lower().startswith("erniebot"):
            api_key = os.environ["ERNIEBOT_API_TOKEN"]
        elif self.model.lower().startswith("warrenq"):
            api_key = os.environ["WARRENQ_API_TOKEN"]
        elif self.model.lower().startswith("giantgpt"):
            api_key = os.environ["GIANTGPT_API_TOKEN"]
        elif self.model.lower().startswith("ruyichat"):
            api_key = os.environ["RUYICHAT_API_TOKEN"]
        elif self.model.lower().startswith("midu"):
            api_key = os.environ["MIDU_API_TOKEN"]
        elif self.model.lower().startswith("yuewriter"):
            api_key = os.environ["YUEWRITER_API_TOKEN"]
        elif self.model.lower().startswith("squirrel"):
            api_key = os.environ["SQUIRREL_API_TOKEN"]
        elif self.model.lower().startswith("xiaohui"):
            api_key = os.environ["XIAOHUI_API_TOKEN"]
        elif self.model.lower().startswith("bigsea"):
            api_key = os.environ["BIGSEA_API_TOKEN"]
        elif self.model.lower().startswith("starbitech"):
            api_key = os.environ["STARBITECH_API_TOKEN"]
        elif self.model.lower().startswith("wind"):
            api_key = os.environ["WIND_API_TOKEN"]

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
        elif self.model.lower() == "eastmoney":
            model = EastMoneyAPILLMModel(**params)
        elif self.model.lower() == "huazang":
            model = HuazhangAPILLMModel(**params)
        elif self.model.lower() == "kkbot":
            model = KKbotAPILLMModel(**params)
        elif self.model.lower() == "wangyi":
            model = WangYiAPILLMModel(**params)
        elif self.model.lower() == "bilibili":
            model = BilibiliAPILLMModel(**params)
        elif self.model.lower() == "infchat":
            model = InfchatAPILLMModel(**params)
        elif self.model.lower() == "caozhi":
            model = CaozhiAPILLMModel(**params)
        elif self.model.lower() == "xiaohongshu":
            model = XiaoHongShuAPILLMModel(**params)
        elif self.model.lower() == "shangtang":
            model = ShangtangAPILLMModel(**params)
        elif self.model.lower() == "claude2":
            model = Claude2APILLMModel(**params)
        elif self.model.lower() == "minimax":
            model = MinimaxAPILLMModel(**params)
        elif self.model.lower() == "erniebot":
            model = ERNIEBOTAPILLMModel(**params)
        elif self.model.lower() == "warrenq":
            model = WarrenQAPILLMModel(**params)
        elif self.model.lower() == "giantgpt":
            model = GiantgptAPILLMModel(**params)
        elif self.model.lower().startswith("ruyichat"):
            model = RuyichatAPILLMModel(**params)
        elif self.model.lower().startswith("midu"):
            model = MiduAPILLMModel(**params)
        elif self.model.lower().startswith("yuewriter"):
           model = YueWriterAPILLMModel(**params)
        elif self.model.lower().startswith("squirrel"):
           model = SquirrelAPILLMModel(**params)
        elif self.model.lower().startswith("xiaohui"):
           model = XiaohuiAPILLMModel(**params)
        elif self.model.lower().startswith("bigsea"):
           model = BigSeaAPILLMModel(**params)
        elif self.model.lower().startswith("starbitech"):
            model = StarbitechAPILLMModel(**params)
        elif self.model.lower().startswith("wind"):
            model = WindAPILLMModel(**params)
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
