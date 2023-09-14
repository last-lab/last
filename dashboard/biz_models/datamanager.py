from tortoise import Model, fields

from dashboard.enums import EvaluationType


class EvaluationPlan(Model):
    """
    评测方案管理model
    """

    name = fields.CharField(max_length=200)
    eval_type = fields.IntEnumField(
        EvaluationType, description="Eval Type", default=EvaluationType.auto_ai_critique
    )
    dimensions = fields.CharField(max_length=500)
    dataset_ids = fields.CharField(max_length=200)
    current_dataset_index = fields.CharField(max_length=200, null=True)
    current_dataset_iter = fields.CharField(max_length=200, null=True)
    uid = fields.CharField(max_length=200, null=True)
    description = fields.CharField(max_length=200, null=True)
    creator = fields.CharField(max_length=200, null=True)
    editor = fields.CharField(max_length=200, null=True)
    reviewer = fields.CharField(max_length=200, null=True)
    permissions = fields.CharField(max_length=200, null=True)
    created_at = fields.DatetimeField(null=True)
    updated_at = fields.DatetimeField(null=True)


class DataSet(Model):
    name = fields.CharField(max_length=200)
    dimensions = fields.CharField(max_length=200, null=True)
    url = fields.CharField(max_length=200, null=True)
    file = fields.CharField(max_length=200, null=True)
    volume = fields.CharField(max_length=200, null=True)
    used_by = fields.CharField(max_length=200, null=True)
    qa_records = fields.CharField(max_length=200, null=True)
    conversation_start_id = fields.CharField(max_length=200, null=True)
    current_conversation_index = fields.IntField(null=True)
    current_qa_record_id = fields.IntField(null=True)
