import os

from last.types.dataset import Dataset
from last.types.public import ReturnCode

def test_create_from_file():
    file_path = os.path.join("docs", "examples", "testset.csv")
    dataset = Dataset.create_from_file(file_path)
    assert dataset.qa_num == 15
    assert dataset.volume == "10.6GB"
    assert dataset.word_cnt == 100000
    assert len(dataset.focused_risks) == 13

    return_code = Dataset.create_from_file(file_path) # 文件重复上传
    assert str(return_code) == "Error 101: Already Exist"
    assert return_code == ReturnCode.ALREADY_EXIST
