from tortoise import Model, fields


class TaskManage(Model):
    task_id = fields.CharField(max_length=50)
    task_type = fields.CharField(max_length=50)
    labeling_method = fields.CharField(max_length=255)
    current_status = fields.CharField(max_length=50)
    dateset = fields.CharField(max_length=255) # 这个任务对应的dataset的id，
    create_time = fields.DateField()
    end_time = fields.DateField()
    assgin_user = fields.CharField(max_length=50)
