from tortoise import Model, fields


class Risk(Model):
    risk_level = fields.IntField()
    risk_id = fields.CharField(max_length=200)
    risk_name = fields.CharField(max_length=200)
    risk_description = fields.TextField(null=True)
    parent_risk_id = fields.CharField(max_length=200, null=True)
    third_risk = fields.CharField(max_length=200, null=True)
