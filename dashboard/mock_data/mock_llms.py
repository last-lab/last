from tortoise import Tortoise

from dashboard.biz_models.eval_model import ModelInfo


async def create_mock_llms():
    connection = Tortoise.get_connection("default")
    await connection.execute_query(f"DROP TABLE IF EXISTS {ModelInfo.__name__.upper()}")
    await Tortoise.generate_schemas(ModelInfo)

    await ModelInfo.create(
        name="gpt-3.5-turbo",
        endpoint="gpt-3.5-turbo",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="3.5.0",
        base_model="GPT3.5-Turbo",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="OpenAI",
        auth_status=True,
    )

    await ModelInfo.create(
        name="gpt-4",
        endpoint="gpt-4",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="4.0",
        base_model="GPT4",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="OpenAI",
        auth_status=True,
    )

    # await ModelInfo.create(
    #     name="alles-chatgpt",
    #     endpoint="alles-chatgpt",
    #     access_key="None",
    #     secret_key="None",
    #     model_type="聊天机器人、自然语言处理助手",
    #     version="3.5.0",
    #     base_model="未知",
    #     parameter_volume="未知",
    #     pretraining_info="未知",
    #     finetuning_info="未知",
    #     alignment_info="未知",
    # )

    # await ModelInfo.create(
    #     name="alles-minimax",
    #     endpoint="alles-minimax",
    #     access_key="None",
    #     secret_key="None",
    #     model_type="聊天机器人、自然语言处理助手",
    #     version="3.5.0",
    #     base_model="未知",
    #     parameter_volume="未知",
    #     pretraining_info="未知",
    #     finetuning_info="未知",
    #     alignment_info="未知",
    # )

    # await ModelInfo.create(
    #     name="alles-gpt4",
    #     endpoint="alles-gpt4",
    #     access_key="None",
    #     secret_key="None",
    #     model_type="聊天机器人、自然语言处理助手",
    #     version="3.5.0",
    #     base_model="未知",
    #     parameter_volume="未知",
    #     pretraining_info="未知",
    #     finetuning_info="未知",
    #     alignment_info="未知",
    # )

    # await ModelInfo.create(
    #     name="alles-claude",
    #     endpoint="alles-claude",
    #     access_key="None",
    #     secret_key="None",
    #     model_type="英文聊天机器人",
    #     version="3.5.0",
    #     base_model="未知",
    #     parameter_volume="未知",
    #     pretraining_info="未知",
    #     finetuning_info="未知",
    #     alignment_info="未知",
    # )

    await ModelInfo.create(
        name="Claude2",
        endpoint="Claude2",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="Anthropic",
        auth_status=True,
    )

    await ModelInfo.create(
        name="MiniMax",
        endpoint="Minimax",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="MiniMax",
        auth_status=True,
    )

    await ModelInfo.create(
        name="ERNIEBOT",
        endpoint="ERNIEBOT",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="BaiDu",
        auth_status=True,
    )

    await ModelInfo.create(
        name="warrenq",
        endpoint="warrenq",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="恒生聚源",
        auth_status=True,
    )

    await ModelInfo.create(
        name="giantgpt",
        endpoint="giantgpt",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="巨人网络",
        auth_status=True,
    )

    # await ModelInfo.create(
    #     name="alles-spark",
    #     endpoint="alles-spark",
    #     access_key="None",
    #     secret_key="None",
    #     model_type="聊天机器人、自然语言处理助手",
    #     version="未知",
    #     base_model="未知",
    #     parameter_volume="未知",
    #     pretraining_info="未知",
    #     finetuning_info="未知",
    #     alignment_info="未知",
    # )

    await ModelInfo.create(
        name="huazang",
        endpoint="huazang",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="小i机器人",
        auth_status=True,
    )
    await ModelInfo.create(
        name="KKBot",
        endpoint="KKBot",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="竹间智能",
        auth_status=True,
    )

    await ModelInfo.create(
        name="eastmoney",
        endpoint="eastmoney",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="东方财富",
        auth_status=True,
    )

    await ModelInfo.create(
        name="wuya(权限关闭)",
        endpoint="wuya",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="None",
        auth_status=False,
    )

    await ModelInfo.create(
        name="puyu",
        endpoint="puyu",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
    )

    await ModelInfo.create(
        name="tigerbot",
        endpoint="tigerbot",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="虎博科技",
        auth_status=True,
    )

    await ModelInfo.create(
        name="mita",
        endpoint="mita",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="mita",
        auth_status=True,
    )

    await ModelInfo.create(
        name="bilibili",
        endpoint="bilibili",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="bilibili",
        auth_status=True,
    )

    await ModelInfo.create(
        name="wangyi",
        endpoint="wangyi",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="WangYi",
        auth_status=True,
    )

    await ModelInfo.create(
        name="shangtang",
        endpoint="shangtang",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="ShangTang",
        auth_status=True,
    )

    await ModelInfo.create(
        name="caozhi",
        endpoint="caozhi",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="达观数据",
        auth_status=True,
    )

    await ModelInfo.create(
        name="infchat",
        endpoint="infchat",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="infchat",
        auth_status=True,
    )

    await ModelInfo.create(
        name="squirrel",
        endpoint="squirrel",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="squirrel",
        auth_status=True,
    )

    await ModelInfo.create(
        name="ruyichat",
        endpoint="ruyichat",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="None",
        auth_status=False,
    )

    await ModelInfo.create(
        name="xiaohui",
        endpoint="xiaohui",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="None",
        auth_status=False,
    )

    await ModelInfo.create(
        name="bigsea",
        endpoint="bigsea",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="bigsea",
        auth_status=False,
    )

    await ModelInfo.create(
        name="starbitech",
        endpoint="starbitech",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="starbitech",
        auth_status=False,
    )
    await ModelInfo.create(
        name="midu",
        endpoint="midu",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="None",
        auth_status=False,
    )

    await ModelInfo.create(
        name="warrenq",
        endpoint="warrenq",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="None",
        auth_status=False,
    )

    await ModelInfo.create(
        name="giantgpt",
        endpoint="giantgpt",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="None",
        auth_status=False,
    )

    await ModelInfo.create(
        name="yuewriter",
        endpoint="yuewriter",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="None",
        auth_status=False,
    )

    await ModelInfo.create(
        name="xiaohongshu",
        endpoint="xiaohongshu",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="XiaoHongShu",
        auth_status=True,
    )

    await ModelInfo.create(
        name="jieyue(key过期)",
        endpoint="jieyue",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="未知",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="None",
        auth_status=False,
    )
