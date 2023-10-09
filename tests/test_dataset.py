import os

import pytest

from last.types.dataset import Dataset


@pytest.mark.skip(reason="data format TBD")
def test_create_from_file():
    file_path = os.path.join("docs", "examples", "testset1.csv")
    dataset = Dataset.create_from_file(file_path)
    assert dataset.qa_num == 15
    assert dataset.volume == "10.6GB"
    assert dataset.word_cnt == 100000
