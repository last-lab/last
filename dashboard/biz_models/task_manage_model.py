from tortoise import Model, fields


class TaskManage(Model):
    task_id = fields.CharField(max_length=50)
    labeling_method = fields.CharField(max_length=255)
    dateset = fields.CharField(max_length=255)
    create_time = fields.DateField()
    current_status = fields.CharField(max_length=50)
    
class LabelResult(Model):
    annotation_task_id = fields.CharField(max_length=50) # 任务ID
    creator = fields.CharField(max_length=50) # 创建人
    create_time = fields.DateField(max_length=50) 
    update_time = fields.DateField(max_length=50)
    annotation_value = fields.CharField(max_length=500)
    sub_task_state = fields.CharField(max_length=50) # 标注任务是否完成
    permission = fields.CharField(max_length=50) # 标注权限
    
    
    