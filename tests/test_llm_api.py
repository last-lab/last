"""
    Before running this test, please add the API key to the os.environ.
"""
import asyncio
import os
import time

import unittest

from last.client.call_llm import generate

# set the API key

os.environ[
    "ALLES_API_TOKEN"
] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Inh1anVuIiwiYXBwbHlfYXQiOjE2ODU0MzIyNTEwNTMsImV4cCI6MTg2Njg3MjI1MX0.J5gCD0yLYkKOmQKDNzidG3FsPz1V0TErn3xASA6m0-0"
os.environ["PUYU_API_TOKEN"] = ""
os.environ[
    "TIGERBOT_API_TOKEN"
] = "2dc003e5bd4ad9c66fbf05c4c9afd61922526dcfabe79d7673d66e1e51e901e9"
os.environ["JIEYUE_API_TOKEN"] = "AI-ONE-b435cad86e273c97b08278dd34ecc378"
os.environ["MITA_API_TOKEN"] = "47d10a183d75b780"
os.environ["WUYA_API_TOKEN"] = ""
os.environ["SOUL_API_TOKEN"] = "5BYMg48N1iYimDsr5kOT"


async def generation_test(prompt, model):
    prompt = prompt
    model = model
    system_prompt = None
    maximum_length = 1000
    temperature = 0.1
    stop_sequence = None
    top_p = 0.9
    frequence_penalty = 0.0
    presence_penalty = 0.0

    generated_text = await generate(
        prompt,
        model,
        system_prompt,
        maximum_length,
        temperature,
        stop_sequence,
        top_p,
        frequence_penalty,
        presence_penalty,
    )

    return generated_text


# @unittest.skip("Need apikey")
class TestLLMAPI(unittest.TestCase):
    def test_tigerbot_api(self):
        generated_text = asyncio.run(
            generation_test(prompt="中国的首都在哪里", model="tigerbot")
        )

        assert generated_text.startswith("北京")

    def test_soul_api(self):
        generated_text = asyncio.run(generation_test(prompt="最近在做什么呀", model="soul"))
        # 大小写都可以， eg. SOUL, Soul
        # print("\nSoul: %s\n" % generated_text)
        assert generated_text is not None

    def test_mita_api(self):
        generated_text = asyncio.run(generation_test(prompt="生日快乐", model="Mita"))
        # 大小写都可以， eg. MITA、mita

        assert generated_text.startswith("生日快乐")

    def test_jieyue_api(self):
        generated_text = asyncio.run(generation_test(prompt="生日快乐", model="JieYue"))
        # 大小写都可以， eg. JIEYUE、jieyue

        assert generated_text is not None

    def test_wuya_api(self):
        generated_text = asyncio.run(generation_test(prompt="投资目标是什么？", model="Wuya"))
        # 大小写都可以， eg. wuya, WUYA

        assert generated_text is not None

    def test_alles_chat_llm_api(self):
        ALLES_CHAT_LLM = [
            "alles-minimax",
            "alles-chatgpt",
            "alles-gpt4",
            "alles-palm",
            "alles-claude",  # Only Support English
            # "alles-wenxin",  # 这个暂时无法访问
            "alles-spark",
        ]

        for model in ALLES_CHAT_LLM:
            generated_text = asyncio.run(
                generation_test(prompt="Happy Birthday", model=model)
            )
            # time.sleep(1)  # waiting for the release of resources

            assert generated_text is not None


if __name__ == "__main__":
    unittest.main()