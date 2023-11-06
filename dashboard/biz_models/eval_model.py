# 这个类里面的东西是专门用来display的
from tortoise import Model, fields

from dashboard.enums import EvalStatus


# 每个评测模型的信息
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


# 每个评测记录的信息
class Record(Model):
    eval_models = fields.CharField(max_length=200, null=True)
    llm_name = fields.CharField(max_length=2000, null=True)
    llm_id = fields.CharField(max_length=2000, null=True)
    eval_plan = fields.CharField(description="Choose evaluation plan", max_length=200, null=True)
    plan_id = fields.IntField(null=True)
    created_at = fields.IntField(null=True, auto_now_add=True)
    state: EvalStatus = fields.IntEnumField(EvalStatus, default=EvalStatus.on_progress, null=True)
    report = fields.BinaryField(null=True)
    created_user_id = fields.CharField(max_length=200)


# id 行记录id
# record_id 评测记录id
# eval_model_id 评测模型id
# risk_id 风险类型id, 综合默认为0，就是综合维度评分，
# score 评分
# eval_data_set_score_json json类型 [{数据集得分信息}] 综合评分留空字段
class ModelResult(Model):
    record_id = fields.IntField()
    eval_model_id = fields.IntField()
    risk_id = fields.IntField()
    score = fields.IntField()
    eval_data_set_score_json = fields.TextField(null=True)


# record_id 评测记录id
# eval_model_id 评测模型id
# risk_id 风险类型id
# score 评分
# come_dataset_id 来源数据集id
# content 案例内容
class ModelRelateCase(Model):
    record_id = fields.IntField()
    eval_model_id = fields.IntField()
    risk_id = fields.IntField()
    score = fields.IntField()
    come_dataset_id = fields.IntField()
    content = fields.TextField()
