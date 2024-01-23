import pandas as pd


def read_data(filename):
    df = pd.read_excel(filename)
    data_list = []
    for item in df["Question"]:
        data_list.append({"role": "user", "content": item})
    return data_list
