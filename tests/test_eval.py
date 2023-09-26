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
                    "focused_risks": '[{"level":1,"name":"国家安全","description":null},{"level":2,"name":"颠覆国家政权","description":null,"downlevel_risk_name":["暴力政治活动"]},{"level":2,"name":"宣扬恐怖主义","description":null,"downlevel_risk_name":["暴力恐吓手段","恐怖袭击策划"]},{"level":2,"name":"挑拨民族对立","description":null,"downlevel_risk_name":[]}]',
                },
                {
                    "name": "test2",
                    "file": os.path.join("docs", "examples", "testset2.csv"),
                    "focused_risks": '[{"level":1,"name":"国家安全","description":null},{"level":2,"name":"颠覆国家政权","description":null,"downlevel_risk_name":["暴力政治活动"]},{"level":2,"name":"宣扬恐怖主义","description":null,"downlevel_risk_name":["暴力恐吓手段","恐怖袭击策划"]},{"level":2,"name":"挑拨民族对立","description":null,"downlevel_risk_name":[]}]',
                },
            ],
            "$llm_model": {
                "name": "PuYu",
                "endpoint": "https://puyu.openxlab.org.cn/puyu/api/v1/chat/completion",
                "access_key": "xxx",
            },
            "$critic_model": {
                "name": "GPT-3.5-Turbo",
                "endpoint": "https://puyu.openxlab.org.cn/puyu/api/v1/chat/completion",
                "access_key": "xxx",
            },
            "$plan": {"name": "SafetyTest"},
        }
    )
    Client.execute(AI_eval, kwargs_json)
