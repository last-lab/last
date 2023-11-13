from io import BytesIO

import pandas as pd


def split_string_to_list(file_name, qa_records_stream):
    if "csv" in file_name:
        return split_csv_file(qa_records_stream)
    elif "xlsx" in file_name:
        return split_xlsx_file(qa_records_stream)
    else:
        return None


def split_csv_file(qa_records_stream):
    csv_data = pd.read_csv(BytesIO(qa_records_stream))
    return [tuple(row) for row in csv_data.values]


def split_xlsx_file(qa_records_stream):
    excel_data = pd.read_excel(BytesIO(qa_records_stream), sheet_name=None)
    sheets = list(excel_data.keys())
    data = []

    for sheet in sheets:
        sheet_data = excel_data[sheet]
        rows = [tuple(row) for row in sheet_data.values]
        data = data + rows

    return data
