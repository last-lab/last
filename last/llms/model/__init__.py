


def init_api_models(settings):
    
    model_list = {}

    for setting in settings:
        if setting["type"] == "openai":
            from .openai_api_model import OpenaiAPILLMModel
            params = {
                "api_key": setting["api_key"],
                "api_base": setting["api_base"],
            }
            model = OpenaiAPILLMModel(**params)
        
        elif setting["type"] == "tiger":
            from .http_tiger_api_model import TigerAPILLMModel
            params = {
                "api_key": setting["api_key"],
                "api_base": setting["api_base"],
            }
            model = TigerAPILLMModel(**params)

        elif setting["type"] == "puyu":
            from .http_puyu_api_model import PuyuAPILLMModel
            params = {
                "api_key": setting["api_key"],
            }
            if setting["api_base"] == "puyu":
                model = PuyuAPILLMModel(**params)

        elif setting["type"] == "alles":
            from .http_alles_api_model import AllesMinimaxAPILLMModel, AllesChatGPTAPILLMModel, AllesGPT4APILLMModel, AllesPalmAPILLMModel, AllesClaudeAPILLMModel, AllesWenxinAPILLMModel, AllesSparkAPILLMModel, AllesBaiduTranslateAPILLMModel
            params = {
                "api_key": setting["api_key"],
            }
            if setting["api_base"] == "minimax":
                model = AllesMinimaxAPILLMModel(**params)
            elif setting["api_base"] == "chatgpt":
                model = AllesChatGPTAPILLMModel(**params)
            elif setting["api_base"] == "gpt4":
                model = AllesGPT4APILLMModel(**params)
            elif setting["api_base"] == "palm":
                model = AllesPalmAPILLMModel(**params)
            elif setting["api_base"] == "claude":
                model = AllesClaudeAPILLMModel(**params)
            elif setting["api_base"] == "wenxin":
                model = AllesWenxinAPILLMModel(**params)
            elif setting["api_base"] == "spark":
                model = AllesSparkAPILLMModel(**params)
            elif setting["api_base"] == "baidu_translate":
                model = AllesBaiduTranslateAPILLMModel(**params)
            else:
                raise NotImplementedError()

        else:
            raise NotImplementedError()
        
        model_list[setting["index"]] = model

    return model_list