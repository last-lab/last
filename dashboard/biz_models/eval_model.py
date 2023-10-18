# 这个类里面的东西是专门用来display的
from tortoise import Model, fields

from dashboard.enums import EvalStatus


class ModelInfo(Model):
    name = fields.CharField(max_length=200, null=True)
    model_type = fields.CharField(max_length=200, null=True)
    version = fields.CharField(max_length=200, null=True)
    base_model = fields.CharField(max_length=200, null=True)
    parameter_volume = fields.CharField(max_length=200, null=True)
    pretraining_info = fields.CharField(max_length=200, null=True)
    finetuning_info = fields.CharField(max_length=200, null=True)
    alignment_info = fields.CharField(max_length=200, null=True)
    endpoint = fields.CharField(max_length=200, null=True)
    access_key = fields.CharField(max_length=2000, null=True)
    secret_key = fields.CharField(max_length=200, null=True)


class Record(Model):
    eval_models = fields.CharField(max_length=200, null=True)
    llm_name = fields.CharField(max_length=200, null=True)
    llm_id = fields.IntField(null=True)
    eval_plan = fields.CharField(description="Choose evaluation plan", max_length=200, null=True)
    plan_id = fields.IntField(null=True)
    created_at = fields.IntField(null=True, auto_now_add=True)
    state: EvalStatus = fields.IntEnumField(EvalStatus, default=EvalStatus.on_progress, null=True)
    report = fields.BinaryField(null=True)


# id 行记录id
# llm_id 评测报告id
# eval_model_name 评测模型名字
# eval_type 评测类型id, 综合默认为0
# score 评分
# eval_data_set_score_json json类型 [{评测集得分信息}] 综合评分留空字段
class ModelResult(Model):
    llm_id = fields.IntField()
    eval_model_name = fields.CharField(max_length=200)
    eval_type_id = fields.IntField()
    score = fields.IntField()
    eval_data_set_score_json = fields.TextField(null=True)


# llm_id 评测报告id
# eval_model_name 评测模型名字
# risk_type 风险类型
# score 评分
# come_dataset_id 来源评测集id
# content 案例内容
class ModelRelateCase(Model):
    llm_id = fields.IntField()
    eval_model_name = fields.CharField(max_length=200)
    risk_type = fields.IntField()
    score = fields.IntField()
    come_dataset_id = fields.IntField()
    content = fields.TextField()