from .dataset import Message
import pandas as pd
from last.types.sensitive_shuffle import SensitiveShuffle

import last.types.llm as llm
scripts = {
    "1": "p1",
    "2": "p2",
    "3": "p3",
    "4": "p4",
    "5": "p5",
    "6": "p6",
    "7": "p7",
}

class PromptGenerator(object):
    """ 不同的问题需要使用不同的prompt模版来描述 
        该脚本生成不同的prompt模版
    """    
    @staticmethod
    def generate_system_prompt(model_name: str, model_type: str, *msgs: Message) -> str:
        """ 用外部脚本生成 prompt
        当前仅考虑为 gpt-4 生成 system_prompt

        Returns:
            str: system prompt
        """        
        prompt = None
        if model_type is llm.LLMType.critic:
            (question, response, correct_ans, sheet_name, prompt_id) = msgs[0]
            if model_name == "gpt-4":
                try:
                    prompt_id = prompt_id.content
                    module_name = scripts[prompt_id]
                    module = __import__("last.newevaluate.messages." + module_name, fromlist=['generate_message'])
                    generate_message = getattr(module, "generate_message")
                    if prompt_id == "1":
                        messages, _ = generate_message(question.content, response.content, sheet_name.content, SensitiveShuffle.get_sensitive_data())
                    else:
                        messages, _ = generate_message(question.content, response.content, sheet_name.content)
                    print("********************************")
                    print(messages)
                    prompt = messages[0]["content"]
                except Exception as e:
                    print("generate critic system prompt error: %s" % e)
        else:
            pass
        return prompt
    
    @staticmethod
    def generate_prompt(model_name: str, model_type: str, *msgs: Message):
        """生成 
        system_prompt
        user prompt: 1. 普通prompt; 2. critic prompt

        Args:
            model_name (str)
            model_type (str): 根据该字段判断是否需要生成 critic prompt
            *msgs (Message): (question: Message, response: Message, correct_ans: Message, sheet_name: Message, prompt_id: Message)
        Returns:
            (system_prompt, prompt) (str, str): 生成的prompt
        """        
        # 先mock一下
        prompt = None
        if model_type is llm.LLMType.critic:
            prompt = PromptGenerator.gen_critic_prompt(*msgs)
        else:
            prompt = msgs[0].content
        
        system_prompt = PromptGenerator.generate_system_prompt(model_name, model_type, msgs)
        return system_prompt, prompt
    
    @staticmethod
    def gen_critic_prompt(question: Message, response: Message, correct_ans: Message, sheet_name: Message, prompt_id: Message) -> str:
        """critic prompt 当前通过外部脚本生成

        Args:
            question (Message): 测试问题
            response (Message): 待测模型回答内容
            correct_ans (Message): 人工标准回答
            sheet_name (Message): 包装成 Message 的 excel 子表名, 标注当前 question 的主题

        Returns:
            str: critic model 的 prompt
        """
        prompt = None
        try:
            prompt_id = prompt_id.content
            module_name = scripts[prompt_id]
            module = __import__("last.newevaluate.messages." + module_name, fromlist=['generate_message'])
            generate_message = getattr(module, "generate_message")
            if prompt_id == "1":
                messages, _ = generate_message(question.content, response.content, sheet_name.content, SensitiveShuffle.get_sensitive_data())
            else:
                messages, _ = generate_message(question.content, response.content, sheet_name.content)
            print("********************************")
            print(messages)
            prompt = messages[1]["content"]
        except Exception as e:
            print("generate critic normal prompt error: %s" % e)
        
        return prompt
    