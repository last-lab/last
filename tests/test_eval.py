# TODO client的部分、ORM的部分没有实现，LLM的调用是MOCK的
import json
import os

from last.client import AI_eval, Client

# 一个task需要plan+model，plan需要dataset


def test_create_eval():
    kwargs_json = json.dumps(
        {
            "$datasets": [
                {
                    "name": "test1",
                    "file": os.path.join("docs", "examples", "testset1.csv"),
                },
                {
                    "name": "test2",
                    "file": os.path.join("docs", "examples", "testset2.csv"),
                },
            ],
            "$llm_model": {"name": "PuYu", "endpoint": "xxx", "access_key": "xxx"},
            "$critic_model": {
                "name": "GPT-3.5-Turbo",
                "endpoint": "xxx",
                "access_key": "xxx",
            },
            "$plan": {"name": "SafetyTest"},
        }
    )
    Client.execute(AI_eval, kwargs_json)
