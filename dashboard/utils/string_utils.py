import re


def split_string_to_list(qa_records):
    text = qa_records.split("\r\n", 1)[1]

    pattern = r"(.*?),(.*)\r\n"  # 匹配问题和答案的模式
    matches = re.findall(pattern, text)

    questions_answers_list = []

    for match in matches:
        question = match[0]
        answer = match[1]
        questions_answers_list.append((question, answer))
    return questions_answers_list
