import ast
import html

risk_level_dict = {"高度敏感": 1, "中度敏感": 2, "低度敏感": 3, "中性词": 4}


def statistic_dataset(dataset_path):
    # 传入一个文件的路径，然后读取一系列的统计数据填充dataset
    # 返回这个数据的大小volume, qa_num，word_cnt，qa_records几个数据
    volume = ("1GB",)
    qa_num = (10,)
    word_cnt = (200,)
    qa_records = """
                Who painted the Mona Lisa?,Leonardo da Vinci
                What is the symbol for the chemical element iron?,Fe
                "Who wrote the play ""Hamlet""?",William Shakespeare
                What is the largest planet in our solar system?,Jupiter
                Who is the author of the Harry Potter book series?,J.K. Rowling
                What is the square root of 64?,8
                In which country is the Taj Mahal located?,India
                Who is the current President of the United States?,Joe Biden
                What is the chemical formula for water?,H2O
                "Which animal is known as the ""King of the Jungle""?",Lion
                What is the tallest mountain in the world?,Mount Everest
                Who invented the telephone?,Alexander Graham Bell
                What is the primary language spoken in Brazil?,Portuguese
                Who painted the ceiling of the Sistine Chapel?,Michelangelo"""
    return (volume, qa_num, word_cnt, qa_records)


def convert_labelstudio_result_to_string(labeling_method, labeling_result_list, risk_level):
    # TODO，目前就实现了当使用了判断标注的流程
    _labeling_method = eval(html.unescape(labeling_method))
    if _labeling_method == ["判断标注"]:
        # TODO，这个函数需要修改
        refine_result = labeling_result_list[0]["value"]["choices"][0]
    elif _labeling_method == ["选择标注"]:
        pass

    elif _labeling_method == ["框选标注"]:
        pass

    elif _labeling_method == ["风险判别"]:
        if risk_level == "0级风险":
            # refine_result = {"0级风险": labeling_result_list[0]["value"]["choices"][0]}
            refine_result = {
                "风险程度": risk_level_dict[labeling_result_list[0]["value"]["choices"][0]]
            }
        elif risk_level == "一级风险":
            refine_result = {"一级风险": labeling_result_list[0]["value"]["choices"][0]}

        elif risk_level == "二级风险":
            refine_result = {}
            for labeling_result in labeling_result_list:
                if "grade_one" in labeling_result["from_name"]:
                    refine_result["一级风险"] = labeling_result["value"]["choices"][0]
                else:
                    refine_result["二级风险"] = labeling_result["value"]["choices"][0]

        elif risk_level == "三级风险":
            refine_result = {}
            for labeling_result in labeling_result_list:
                if "grade_one" in labeling_result["from_name"]:
                    refine_result["一级风险"] = labeling_result["value"]["choices"][0]
                elif "grade_two" in labeling_result["from_name"]:
                    refine_result["二级风险"] = labeling_result["value"]["choices"][0]
                else:
                    refine_result["三级风险"] = labeling_result["value"]["choices"]

        elif risk_level == "风险程度_一级风险":
            refine_result = {}
            for labeling_result in labeling_result_list:
                if labeling_result["from_name"] == "rating":
                    refine_result["风险程度"] = risk_level_dict[labeling_result["value"]["choices"][0]]
                else:
                    refine_result["一级风险"] = labeling_result["value"]["choices"][0]

        elif risk_level == "风险程度_二级风险":
            refine_result = {}
            for labeling_result in labeling_result_list:
                if labeling_result["from_name"] == "rating":
                    refine_result["风险程度"] = risk_level_dict[labeling_result["value"]["choices"][0]]
                elif "grade_one" in labeling_result["from_name"]:
                    refine_result["一级风险"] = labeling_result["value"]["choices"][0]
                else:
                    refine_result["二级风险"] = labeling_result["value"]["choices"][0]

        elif risk_level == "风险程度_三级风险":
            refine_result = {}
            for labeling_result in labeling_result_list:
                if labeling_result["from_name"] == "rating":
                    refine_result["风险程度"] = risk_level_dict[labeling_result["value"]["choices"][0]]
                elif "grade_one" in labeling_result["from_name"]:
                    refine_result["一级风险"] = labeling_result["value"]["choices"][0]
                elif "grade_two" in labeling_result["from_name"]:
                    refine_result["二级风险"] = labeling_result["value"]["choices"][0]
                else:
                    refine_result["三级风险"] = labeling_result["value"]["choices"]

    elif _labeling_method == ["安全回答"]:
        refine_result = labeling_result_list[0]["value"]["text"]
    return refine_result


def update_labeling_result(user_id: str, new_labeling_result: str, current_labeling_result: str):
    string_result_to_dict = ast.literal_eval(current_labeling_result)
    string_result_to_dict[user_id] = new_labeling_result
    return string_result_to_dict


def concat_labeling_result(user_id, new_labeling_result, current_labeling_result):
    # 这个函数是将两个标注结果合并起来
    pass


def convert_table_to_csv(table):
    # 这个函数是将标注结果变成csv文件，然后返回
    pass


def convert_audit_data(labeling_method, audit_result, risk_level):
    if labeling_method == "判断标注":
        # TODO，这个函数需要修改
        refine_result = audit_result["0"]

    elif labeling_method == "选择标注":
        pass

    elif labeling_method == "框选标注":
        pass

    elif labeling_method == "风险判别":
        if risk_level == "0级风险":
            refine_result = {"风险程度": risk_level_dict[audit_result["0"]]}
        elif risk_level == "一级风险":
            refine_result = {"一级风险": audit_result["0"]}

        elif risk_level == "二级风险":
            refine_result = {}
            refine_result["一级风险"] = audit_result["0"]
            refine_result["二级风险"] = audit_result["1"]

        elif risk_level == "三级风险":
            refine_result = {}
            refine_result["一级风险"] = audit_result["0"]
            refine_result["二级风险"] = audit_result["1"]
            refine_result["三级风险"] = audit_result["2"]

        elif risk_level == "风险程度_一级风险":
            refine_result = {}
            refine_result["风险程度"] = risk_level_dict[audit_result["0"]]
            refine_result["一级风险"] = audit_result["1"]

        elif risk_level == "风险程度_二级风险":
            refine_result = {}
            refine_result["风险程度"] = risk_level_dict[audit_result["0"]]
            refine_result["一级风险"] = audit_result["1"]
            refine_result["二级风险"] = audit_result["2"]

        elif risk_level == "风险程度_三级风险":
            refine_result = {}
            refine_result["风险程度"] = risk_level_dict[audit_result["0"]]
            refine_result["一级风险"] = audit_result["1"]
            refine_result["二级风险"] = audit_result["2"]
            refine_result["三级风险"] = audit_result["3"]

    elif labeling_method == "安全回答":
        refine_result = audit_result["0"]

    return refine_result
