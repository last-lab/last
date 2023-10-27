from tortoise import Model, fields


class AuditPage(Model):
    task_id = fields.CharField(max_length=50)
    end_time = fields.DateField()
    labeling_method = fields.CharField(max_length=255)
    audit_user = fields.CharField(max_length=255)
    audit_length = fields.CharField(max_length=255)
    audit_progress = fields.CharField(max_length=255)


class AuditResult(Model):
    task_id = fields.CharField(max_length=50)
    status = fields.CharField(max_length=50)
    question_id = fields.IntField(null=True)
    audit_user = fields.CharField(max_length=255)
    question = fields.CharField(max_length=255)
    answer = fields.CharField(max_length=255)
