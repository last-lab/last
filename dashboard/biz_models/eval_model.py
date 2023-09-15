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
    access_key = fields.CharField(max_length=200, null=True)
    secret_key = fields.CharField(max_length=200, null=True)


class Record(Model):
    eval_models = fields.CharField(max_length=200, null=True)
    llm_name = fields.CharField(max_length=200, null=True)
    llm_id = fields.IntField(null=True)
    eval_plan = fields.CharField(description="Choose evaluation plan", max_length=200, null=True)
    plan_id = fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    state: EvalStatus = fields.IntEnumField(EvalStatus, default=EvalStatus.on_progress, null=True)
    report = fields.BinaryField(null=True)
