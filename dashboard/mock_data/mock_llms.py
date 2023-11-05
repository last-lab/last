from tortoise import Tortoise

from dashboard.biz_models.eval_model import ModelInfo


async def create_mock_llms():
    connection = Tortoise.get_connection("default")
    await connection.execute_query(f"DROP TABLE IF EXISTS {ModelInfo.__name__.upper()}")
    await Tortoise.generate_schemas(ModelInfo)

    # await ModelInfo.create(
    #     name="gpt-3.5-turbo",
    #     endpoint="gpt-3.5-turbo",
    #     access_key="None",
    #     secret_key="None",
    #     model_type="聊天机器人、自然语言处理助手",
    #     version="3.5.0",
    #     base_model="GPT3.5-Turbo",
    #     parameter_volume="约50亿",
    #     pretraining_info="包含约7500亿个英文和中文字词的大规模无标签文本数据集",
    #     finetuning_info="未经过微调",
    #     alignment_info="RLHF对齐",
    # )

    # await ModelInfo.create(
    #     name="gpt-4",
    #     endpoint="gpt-4",
    #     access_key="None",
    #     secret_key="None",
    #     model_type="聊天机器人、自然语言处理助手",
    #     version="3.5.0",
    #     base_model="GPT3.5-Turbo",
    #     parameter_volume="约50亿",
    #     pretraining_info="包含约7500亿个英文和中文字词的大规模无标签文本数据集",
    #     finetuning_info="未经过微调",
    #     alignment_info="RLHF对齐",
    # )

    await ModelInfo.create(
        name="alles-chatgpt",
        endpoint="alles-chatgpt",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="3.5.0",
        base_model="GPT3.5-Turbo",
        parameter_volume="约50亿",
        pretraining_info="包含约7500亿个英文和中文字词的大规模无标签文本数据集",
        finetuning_info="未经过微调",
        alignment_info="RLHF对齐",
    )

    await ModelInfo.create(
        name="alles-minimax",
        endpoint="alles-minimax",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="3.5.0",
        base_model="GPT3.5-Turbo",
        parameter_volume="约50亿",
        pretraining_info="包含约7500亿个英文和中文字词的大规模无标签文本数据集",
        finetuning_info="未经过微调",
        alignment_info="RLHF对齐",
    )

    await ModelInfo.create(
        name="alles-gpt4",
        endpoint="alles-gpt4",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="3.5.0",
        base_model="GPT3.5-Turbo",
        parameter_volume="约50亿",
        pretraining_info="包含约7500亿个英文和中文字词的大规模无标签文本数据集",
        finetuning_info="未经过微调",
        alignment_info="RLHF对齐",
    )

    # await ModelInfo.create(
    #     name="alles-palm",
    #     endpoint="alles-palm",
    #     access_key="None",
    #     secret_key="None",
    #     model_type="聊天机器人、自然语言处理助手",
    #     version="3.5.0",
    #     base_model="GPT3.5-Turbo",
    #     parameter_volume="约50亿",
    #     pretraining_info="包含约7500亿个英文和中文字词的大规模无标签文本数据集",
    #     finetuning_info="未经过微调",
    #     alignment_info="RLHF对齐",
    # )

    await ModelInfo.create(
        name="alles-claude",
        endpoint="alles-claude",
        access_key="None",
        secret_key="None",
        model_type="英文聊天机器人",
        version="3.5.0",
        base_model="",
        parameter_volume="约50亿",
        pretraining_info="包含约7500亿个英文和中文字词的大规模无标签文本数据集",
        finetuning_info="未经过微调",
        alignment_info="RLHF对齐",
    )

    # await ModelInfo.create(
    #     name="alles-wenxin",
    #     endpoint="alles-wenxin",
    #     access_key="None",
    #     secret_key="None",
    #     model_type="聊天机器人、自然语言处理助手",
    #     version="3.5.0",
    #     base_model="GPT3.5-Turbo",
    #     parameter_volume="约50亿",
    #     pretraining_info="包含约7500亿个英文和中文字词的大规模无标签文本数据集",
    #     finetuning_info="未经过微调",
    #     alignment_info="RLHF对齐",
    # )

    await ModelInfo.create(
        name="alles-spark",
        endpoint="alles-spark",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="3.5.0",
        base_model="GPT3.5-Turbo",
        parameter_volume="约50亿",
        pretraining_info="包含约7500亿个英文和中文字词的大规模无标签文本数据集",
        finetuning_info="未经过微调",
        alignment_info="RLHF对齐",
    )

    await ModelInfo.create(
        name="wuya(权限关闭)",
        endpoint="wuya",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="3.5.0",
        base_model="GPT3.5-Turbo",
        parameter_volume="约50亿",
        pretraining_info="包含约7500亿个英文和中文字词的大规模无标签文本数据集",
        finetuning_info="未经过微调",
        alignment_info="RLHF对齐",
    )

    # await ModelInfo.create(
    #     name="puyu",
    #     endpoint="puyu",
    #     access_key="None",
    #     secret_key="None",
    #     model_type="聊天机器人、自然语言处理助手",
    #     version="3.5.0",
    #     base_model="GPT3.5-Turbo",
    #     parameter_volume="约50亿",
    #     pretraining_info="包含约7500亿个英文和中文字词的大规模无标签文本数据集",
    #     finetuning_info="未经过微调",
    #     alignment_info="RLHF对齐",
    # )

    await ModelInfo.create(
        name="tigerbot",
        endpoint="tigerbot",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="3.5.0",
        base_model="GPT3.5-Turbo",
        parameter_volume="约50亿",
        pretraining_info="包含约7500亿个英文和中文字词的大规模无标签文本数据集",
        finetuning_info="未经过微调",
        alignment_info="RLHF对齐",
    )

    await ModelInfo.create(
        name="mita",
        endpoint="mita",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="3.5.0",
        base_model="GPT3.5-Turbo",
        parameter_volume="约50亿",
        pretraining_info="包含约7500亿个英文和中文字词的大规模无标签文本数据集",
        finetuning_info="未经过微调",
        alignment_info="RLHF对齐",
    )

    await ModelInfo.create(
        name="jieyue(key过期)",
        endpoint="jieyue",
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="3.5.0",
        base_model="GPT3.5-Turbo",
        parameter_volume="约50亿",
        pretraining_info="包含约7500亿个英文和中文字词的大规模无标签文本数据集",
        finetuning_info="未经过微调",
        alignment_info="RLHF对齐",
    )
