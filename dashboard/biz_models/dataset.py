from tortoise import Model, fields

class DataSet(Model):
    name = fields.CharField(max_length=200)
    focused_risks = fields.CharField(max_length=2000, null=True)
    url = fields.CharField(max_length=200, null=True)
    file = fields.CharField(max_length=200, null=True)
    volume = fields.CharField(max_length=200, null=True)
    used_by = fields.CharField(max_length=200, null=True)
    updated_at = fields.CharField(max_length=200, null=True)
    qa_num = fields.IntField(max_length=200, null=True)
    word_cnt = fields.IntField(max_length=200, null=True)
    qa_records = fields.CharField(max_length=200, null=True)
    conversation_start_id = fields.CharField(max_length=200, null=True)
    current_conversation_index = fields.IntField(null=True)
    current_qa_record_id = fields.IntField(null=True)