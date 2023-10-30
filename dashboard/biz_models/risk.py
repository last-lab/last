from tortoise import Model, fields


# risk_level 风险维度等级
# risk_id 风险维度id
# risk_name 风险维度名称
# risk_description 风险维度描述
# parent_risk_id 父级风险维度（一级维度时留空）
# sensitivity 敏感度
class Risk(Model):
    risk_level = fields.IntField()
    risk_id = fields.CharField(max_length=200)
    risk_name = fields.CharField(max_length=200)
    risk_description = fields.TextField(null=True)
    parent_risk_id = fields.CharField(max_length=200, null=True)
    sensitivity = fields.IntField(null=True)
