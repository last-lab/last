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
