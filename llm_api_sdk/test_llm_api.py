"""
Before running this test, please add the API key to the os.environ.
"""
import asyncio
import unittest
from src.llm_api import TestAPILLMModel


async def generation_test(api_key:str):
    llm_api_test = TestAPILLMModel(api_key)

    resp = await llm_api_test.generate(
        temperature = 0.00001,
        top_p = 0.9,
        frequence_penalty = 0.0,
        presence_penalty = 0.0,
    )
    flag, message = llm_api_test.parse(resp)
    return flag, message


@unittest.skip("Need develop")
class TestLLMAPI(unittest.TestCase):

    def test_tigerbot_api(self):
        flag, generated_text = asyncio.run(
            generation_test(
                api_key='xxx',
            )
        )
        print(generated_text)
        assert flag
        assert generated_text is not None
        assert isinstance(generated_text, str)


if __name__ == "__main__":
    unittest.main()
