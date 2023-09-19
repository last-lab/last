from tortoise import Model, fields


class Risk(Model):
    uid = fields.CharField(max_length=200)
    first_risk = fields.CharField(max_length=200)
    second_risk = fields.CharField(max_length=200)
    third_risk = fields.CharField(max_length=200)
    description = fields.TextField(null=True)
