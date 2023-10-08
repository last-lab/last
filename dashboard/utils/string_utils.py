import re


def split_string_to_list(qa_records):
    pattern = r"<BOS>(.+?)<EOS><BOS>(.+?)<EOS>"  # 匹配问题和答案的模式
    matches = re.findall(pattern, qa_records, re.DOTALL)

    questions_answers_list = []

    for match in matches:
        question = match[0].strip()
        answer = match[1].strip()
        questions_answers_list.append((question, answer))
    return questions_answers_list
