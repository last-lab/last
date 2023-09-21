from tortoise import Model, fields


class TaskManage(Model):
    task_id = fields.CharField(max_length=50)
    labeling_method = fields.CharField(max_length=255)
    dateset = fields.CharField(max_length=255)
    create_time = fields.DateField()
    current_status = fields.CharField(max_length=50)
