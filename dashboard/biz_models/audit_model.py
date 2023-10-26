from tortoise import Model, fields


class AuditResult(Model):
    task_id = fields.CharField(max_length=50)
    current_status = fields.CharField(max_length=50)
    question_id = fields.IntField(null=True)
    question = fields.CharField(max_length=20000, null=True)
    answer = fields.CharField(max_length=20000, null=True)
