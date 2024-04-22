from last.types.dataset import Dataset, QARecord, Message, MessageRole
from last.types.llm import LLM, LLMType
from last.types.plan import EvaluationType, Plan
from last.types.public import ID, Placeholder
from last.types.task import Task
from tqdm import tqdm
import re
import asyncio
import time
from loguru import logger

from .task_list import TaskList

from last.newevaluate.utlis import extract
from last.types.sensitive_shuffle import SensitiveShuffle

async def AI_eval(
    datasets=Placeholder(parser=lambda x: x),
    llm_model=Placeholder(parser=lambda x: x),
    critic_model=Placeholder(parser=lambda x: x),
    plan=Placeholder(parser=lambda x: x),
    prompt=Placeholder(parser=lambda x: x),
):
    datasets = [
        Dataset(
            name=dataset["name"],
            file=dataset["file"],
        )
        for dataset in datasets
    ]

    plan = Plan(
        name=plan["name"],
        eval_type=EvaluationType.auto_ai_critique,
        datasets=datasets,
    )

    llm_model = LLM(
        name=llm_model["name"],
        model_type=LLMType.normal,
        endpoint=llm_model["endpoint"],
        access_key=llm_model["access_key"],
    )

    if plan.eval_type == EvaluationType.auto_ai_critique and critic_model["name"] != 'null':
        critic_model = LLM(
            name=critic_model["name"],
            model_type=LLMType.critic,
            endpoint=critic_model["endpoint"],
            access_key=critic_model["access_key"],
        )
        use_ai_critique = True
    else:
        use_ai_critique = False

    new_qa_records = {}
    progress_bar = tqdm(total=3, desc=llm_model.name + "的评测进度", leave=False)
    
    # 任务队列
    taskList = TaskList()
    # 待测模型的回答
    response_list = []
    # 评测结果
    critic_list = []
    
    for dataset, qa_record in plan:
        question = qa_record.question
        await taskList.append(asyncio.create_task(llm_model(question)))
        
    # 无异常抛出的情况下 response_list 与 task_list 元素一一对应
    response_list = await taskList.get_result_list()
    progress_bar.update(1)
    print(llm_model.name + "的评测进度:待测模型测试完毕")
    
    begin_time = time.time()
    if use_ai_critique:
        ## 敏感词筛选
        sensitive_shuffle_result = [True] * len(response_list)
        # if prompt["id"] == "1":
        #     sensitive_shuffle_result = SensitiveShuffle.sensitive_shuffle(plan, response_list)
            
        # critic任务
        taskList.clear()
        for (dataset, qa_record), response, pass_sensitive_shuffle in zip(plan, response_list, sensitive_shuffle_result):
            question = qa_record.question
            correct_ans = qa_record.answer
            ## sheet_name 作为 theme, 确定 type_prompt
            sheet_name = Message(role=MessageRole.Chat, content=qa_record.sheet_name)
            ## prompt id 索引 使用的具体脚本
            prompt_id = Message(role=MessageRole.Chat, content=prompt["id"])
            if pass_sensitive_shuffle:
                # 通过了敏感词筛选的回答还需要经过LLM审查
                await taskList.append(asyncio.create_task(critic_model(question, response, correct_ans, sheet_name, prompt_id)))

        
        llm_critic_result = await taskList.get_result_list()  # 无异常抛出的情况下 critic_list 与 task_list 元素一一对应
        if critic_model.name == 'puan':
            critic_list = llm_critic_result
        else:
            critic_list = emerge_sensitive_critic_llm_critic(sensitive_shuffle_result, llm_critic_result)
    else:
        critic_list = [Message(role=MessageRole.AI, content="null") for i in range(len(response_list))]
    end_time = time.time()
    logger.info("评判模型评测耗时: {elapsed_time}", elapsed_time=(end_time - begin_time) / 60.0)
    progress_bar.update(1)
    print(llm_model.name + "的评测进度:评判模型评测完毕")

    # 处理评测结果
    for (dataset, qa_record), response, critic_msg in zip(plan, response_list, critic_list):
        question = qa_record.question
        sheet_name = qa_record.sheet_name
        # 外部脚本处理评判结果
        try:
            if critic_model.name == 'puan':
                critic = str(critic_msg)
            else:
                critic = extract(str(critic_msg))
            critic = Message(role=MessageRole.Chat, content=str(critic))
            reason = critic_msg
        except Exception as e:
            # 模型拒绝回答时 评分设为 None
            critic = Message(role=MessageRole.Chat, content="None")
            reason = Message(role=MessageRole.Chat, content="评测模型输出格式异常或未执行自动评测")
        new_qa_record = QARecord(sheet_name=sheet_name, question=question, answer=response, critic=critic, reason=reason)
        new_qa_records[ID()] = new_qa_record
    progress_bar.update(1)
    print(llm_model.name + "的评测进度:评测结果处理完毕")
    progress_bar.close()

    task = Task(
        plan=plan,
        llm_model=llm_model,
        critic_model=critic_model,
        results=new_qa_records,
    )

    new_dataset = Dataset(name=plan.name + "+" + llm_model.name + "+问答记录", qa_records=new_qa_records, file=None)

    return task, new_dataset

def emerge_sensitive_critic_llm_critic(sensitive_shuffle_result, llm_critic_result) -> list:
    """将敏感词筛选的结果和LLM的评测结果结合 构成最终评测结果

    Args:
        sensitive_shuffle_result (list): 敏感词筛选的结果
        llm_critic_result (list): LLM的评测结果

    Returns:
        最终评测结果
    """    
    critic_list = [None] * len(sensitive_shuffle_result)
    llm_critic_result_index = 0
    for i, val in enumerate(sensitive_shuffle_result):
        if val == True:
            # 通过了敏感词检查 最终评判结果使用LLM评判结果
            critic_list[i] = llm_critic_result[llm_critic_result_index]
            llm_critic_result_index += 1
        else:
            # 未通过敏感词检查 直接判为B 未通过
            critic_list[i] = Message(role=MessageRole.AI, content="判断结果: B")
    return critic_list