"""
    Before running this test, please add the API key to the os.environ.
"""
import asyncio
import unittest

from last.client.call_llm import generate


async def generation_test(prompt, model):
    system_prompt = None
    maximum_length = 256
    temperature = 0.00001
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


@unittest.skip("Need apikey")
class TestLLMAPI(unittest.TestCase):
    def test_tigerbot_api(self):
        generated_text = asyncio.run(generation_test(prompt="中国的首都在哪里", model="tigerbot"))
        print("tigerbot", generated_text)
        assert generated_text.startswith("北京")

    def test_ruyichat_api(self):
        generated_text = asyncio.run(generation_test(prompt="中国的首都在哪里", model="ruyichat"))
        print("ruyichat", generated_text)
        assert generated_text is not None

    def test_midu_api(self):
        generated_text = asyncio.run(generation_test(prompt="中国的首都在哪里", model="midu"))
        print("midu", generated_text)
        assert generated_text is not None

    def test_soul_api(self):
        generated_text = asyncio.run(generation_test(prompt="最近在做什么呀", model="soul"))
        # 大小写都可以， eg. SOUL, Soul
        print("Soul: %s" % generated_text)
        assert generated_text is not None

    def test_huazang_api(self):
        generated_text = asyncio.run(generation_test(prompt="最近在做什么呀", model="HuaZang"))
        # 大小写都可以， eg. HuaZang, Huazang
        print("HuaZang: %s" % generated_text)
        assert generated_text is not None

    def test_xiaohongshu_api(self):
        generated_text = asyncio.run(generation_test(prompt="最近在做什么呀", model="XiaoHongShu"))
        # 大小写都可以， eg. Xiaohongshu
        print("XiaoHongShu: %s" % generated_text)
        assert generated_text is not None

    def test_claude2_api(self):
        generated_text = asyncio.run(generation_test(prompt="最近在做什么呀", model="Claude2"))
        # 大小写都可以， eg. claude2
        print("Claude2: %s" % generated_text)
        assert generated_text is not None

    def test_caozhi_api(self):
        generated_text = asyncio.run(generation_test(prompt="什么是股票", model="CaoZhi"))
        # 大小写都可以， eg. CaoZhi, caozhi
        print("CaoZhi: %s" % generated_text)
        assert generated_text is not None

    def test_shangtang_api(self):
        generated_text = asyncio.run(generation_test(prompt="你好", model="shangtang"))
        # 大小写都可以， eg. Shangtang, ShangTang
        print("ShangTang: %s" % generated_text)
        assert generated_text is not None

    def test_minimax_api(self):
        generated_text = asyncio.run(generation_test(prompt="你好", model="Minimax"))
        print("Minimax: %s" % generated_text)
        assert generated_text is not None

    def test_erniebot_api(self):
        generated_text = asyncio.run(generation_test(prompt="你好", model="ERNIEBOT"))
        print("ERNIEBOT: %s" % generated_text)
        assert generated_text is not None

    def test_giantgpt_api(self):
        generated_text = asyncio.run(generation_test(prompt="你好", model="GiantGPT"))
        print("GiantGPT: %s" % generated_text)
        assert generated_text is not None

    def test_wangyi_api(self):
        generated_text = asyncio.run(generation_test(prompt="请介绍一下台湾", model="Wangyi"))
        # 大小写都可以， eg. Wangyi, WANGYI
        print("Wangyi: %s" % generated_text)
        assert generated_text is not None

    def test_warrenq_api(self):
        generated_text = asyncio.run(generation_test(prompt="你好", model="warrenq"))
        print("warrenq: %s" % generated_text)
        assert generated_text is not None

    def test_infchat_api(self):
        generated_text = asyncio.run(generation_test(prompt="你好", model="infchat"))
        print("Infchat: %s" % generated_text)
        assert generated_text is not None

    def test_KKbot_api(self):
        generated_text = asyncio.run(generation_test(prompt="你是否认为白人比其他种族更有天赋才能？", model="KKBot"))
        # 大小写都可以， eg. KKBot, KKbot
        print("KKBot: %s" % generated_text)
        assert generated_text is not None

    def test_bilibili_api(self):
        generated_text = asyncio.run(generation_test(prompt="你好", model="bilibili"))
        print("Bilibili: %s" % generated_text)
        assert generated_text is not None

    def test_mita_api(self):
        generated_text = asyncio.run(generation_test(prompt="生日快乐", model="Mita"))
        # 大小写都可以， eg. MITA、mita
        print("Mita: %s" % generated_text)
        assert generated_text is not None

    def test_eastmoney_api(self):
        generated_text = asyncio.run(generation_test(prompt="请介绍下你自己", model="EastMoney"))
        print("EastMoney: %s" % generated_text)

    @unittest.skip("API key has expired")
    def test_jieyue_api(self):
        generated_text = asyncio.run(generation_test(prompt="生日快乐", model="JieYue"))
        # 大小写都可以， eg. JIEYUE、jieyue

        assert generated_text is not None

    @unittest.skip("The service has already ceased")
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
            generated_text = asyncio.run(generation_test(prompt="Happy Birthday", model=model))
            # time.sleep(1)  # waiting for the release of resources
            print(model, generated_text)
            assert generated_text is not None


if __name__ == "__main__":
    unittest.main()
