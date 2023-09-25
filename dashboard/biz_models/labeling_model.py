from tortoise import Model, fields


class LabelPage(Model):
    task_id = fields.CharField(max_length=50)
    task_type = fields.CharField(max_length=50)
    labeling_method = fields.CharField(max_length=255)
    current_status = fields.CharField(max_length=50)
    dateset = fields.CharField(max_length=255)  # 这个任务对应的dataset的名称
    dataset_uid = fields.CharField(max_length=255)  # 每一个数据集有唯一的uid
    end_time = fields.DateField()


class LabelResult(Model):
    task_id = fields.CharField(max_length=50)  # 任务ID
    dataset_id = fields.CharField(max_length=50)
    creator = fields.CharField(max_length=50)  # 创建人
    question_id = fields.IntField(null=True)
    question = fields.CharField(max_length=200, null=True)
    answer = fields.CharField(max_length=200, null=True)
    labeling_result = fields.CharField(max_length=200, null=True, default=None)
