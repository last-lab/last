# Copyright © 2023 Shanghai AI lab
# All rights reserved.
import asyncio
from pathlib import Path
import unittest
from src.llm_api import TestAPILLMModel
from src.utils import read_data


async def generation_test(data: list):
    api_key = ""

    llm_api_test = TestAPILLMModel(api_key)
    # If you need to add additional variables,
    # please add them here, i.e. temperature, topK
    resp = await llm_api_test.generate(
        messages=data,
    )
    # --------------------------------------------
    flag, message = llm_api_test.parse(resp)
    return flag, message


async def generation_test_with_semaphore(sem, data):
    async with sem:
        return await generation_test(data)


@unittest.skip("Need develop")
class TestLLMAPI(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.current_directory = Path.cwd()
        self.subdirectory = "test_data"
        self.file_name = "dataset.xlsx"

    async def test_bot_api(self):
        full_path = self.current_directory.joinpath(self.subdirectory, self.file_name)
        data_list = read_data(full_path)
        step = 2  # qps

        semaphore = asyncio.Semaphore(step)
        tasks = [
            generation_test_with_semaphore(semaphore, [item]) for item in data_list
        ]
        results = await asyncio.gather(*tasks)

        for result in results:
            flag, generated_text = result
            print(generated_text)
            self.assertTrue(flag)
            self.assertIsNotNone(generated_text)
            self.assertIsInstance(generated_text, str)


if __name__ == "__main__":
    unittest.main()
