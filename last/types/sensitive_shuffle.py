from last.types.plan import Plan
from last.newevaluate.messages.p1 import generate_message
import pandas as pd
import os

class SensitiveShuffle(object):
    """tool class 
    1. 存储敏感词
    2. 根据敏感词库对LLM的回答进行敏感词筛查
    """    
    # 13w条敏感词 约 3mb
    sensitive_data = None
    
    @staticmethod
    def sensitive_shuffle(plan:Plan, answer_list:list) -> list:
        """判断answer中有无敏感词

        Args:
            plan (Plan): 评测方案,其中包含quesiton
            answer_list (list): 待测模型回复内容

        Returns:
            list: True: 通过敏感词筛查; False: 未通过敏感词筛查
        """        
        if SensitiveShuffle.sensitive_data == None:
            SensitiveShuffle.load_sensitive_words()
        
        result_list = []
        for (dataset, qa_record), answer in zip(plan, answer_list):
            question = qa_record.question.content
            answer = answer.content
            (_ ,result) = generate_message(question, answer, "", SensitiveShuffle.sensitive_data)
            result_list.append(result)
        return result_list
    
    @staticmethod
    def load_sensitive_words():
        if SensitiveShuffle.sensitive_data:
            return
        sub_path = "/last/newevaluate/sensitive/"
        sent_all_file_name = "12.5_sensitive_new.csv"
        sent_high_file_name = "12.5_sensitive_high_new.csv"
        current_path = os.getcwd()
        sent_all = pd.read_csv(current_path + sub_path + sent_all_file_name)
        sent_all = list(sent_all['0'])
        sent_high = pd.read_csv(current_path + sub_path + sent_high_file_name)
        sent_high = list(sent_high['0'])
        SensitiveShuffle.sensitive_data = (sent_high, sent_all)
        
    @staticmethod
    def get_sensitive_data():
        if SensitiveShuffle.sensitive_data == None:
            SensitiveShuffle.load_sensitive_words()
        return SensitiveShuffle.sensitive_data
        