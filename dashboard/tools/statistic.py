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


def distribute_labeling_task(len_dataset: int, assign_user_list):
    # 传入的数据为[{"assign_user", 32}]这种格式
    # 采用某种算法，给不同的用户分配不同的item进行标注
    # 返回的结果为 {0: ['user1', 'user2'], ...}
    # 暂时返回每个用户都要标注所有的item
    item_assign_user_dict = {}
    assign_user_item_dict = {}
    for index in range(len_dataset):
        if index % 2 == 0:
            item_assign_user_dict[index] = [assign_item["annotator"] for assign_item in assign_user_list]
        else:
            item_assign_user_dict[index] = []
    # 对这个item_assign_user_dict 进行反序遍历
    for index, assign_user_list in item_assign_user_dict.items():
        if len(assign_user_list) !=0:
            for _assign_user in assign_user_list:
                if _assign_user not in assign_user_item_dict:
                    assign_user_item_dict[_assign_user] = [index]
                else:
                    assign_user_item_dict[_assign_user].append(index)
    # 返回{"user1": 10, "user2": 20, ...}
    assign_user_item_length = {assign_user: len(assign_user_item_dict[assign_user]) for assign_user in assign_user_item_dict}
    return item_assign_user_dict, assign_user_item_dict, assign_user_item_length
