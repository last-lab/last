from tortoise import Model, fields


class LabelPage(Model):
    task_type = fields.CharField(max_length=50)
    labeling_method = fields.CharField(max_length=255)
    release_time = fields.DatetimeField()
    current_status = fields.CharField(max_length=50)