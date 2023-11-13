from tortoise import Model, fields


class TestModel(Model):
    test_id = fields.CharField(max_length=50)
