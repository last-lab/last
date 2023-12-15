from tortoise import Model, fields


class AuditPage(Model):
    task_id = fields.CharField(max_length=50)
    end_time = fields.DateField()
    labeling_method = fields.CharField(max_length=255)
    audit_user = fields.CharField(max_length=25500)
    audit_length = fields.CharField(max_length=25500)
    audit_progress = fields.CharField(max_length=25500)
    audit_flag = fields.CharField(max_length=25500)
    dataset = fields.CharField(max_length=255)


class AuditResult(Model):
    task_id = fields.CharField(max_length=50)
    status = fields.CharField(max_length=50)
    question_id = fields.IntField(null=True)
    audit_user = fields.CharField(max_length=25500)
    question = fields.CharField(max_length=25500)
    answer = fields.CharField(max_length=25500)
    audit_result = fields.CharField(max_length=10000, null=True, default=None)
    sheet_name = fields.CharField(max_length=200)
    model_label = fields.CharField(max_length=25500, null=True, default=None)
    model_reason = fields.CharField(max_length=25500, null=True, default=None)
