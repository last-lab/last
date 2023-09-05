from tortoise import Model, fields

from last.services import enums


class AbstractAdmin(Model):
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=200)
    is_active = fields.BooleanField(
        default=True,
    )
    is_superuser = fields.BooleanField(default=False)
    roles: fields.ManyToManyRelation["AbstractRole"]

    class Meta:
        abstract = True


class AbstractResource(Model):
    label = fields.CharField(max_length=50, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.pk} - {self.label}"


class AbstractPermission(Model):
    label = fields.CharField(max_length=50)
    resource = fields.CharField(max_length=50)
    permission = fields.CharEnumField(enums.Permission, default=enums.Permission.read)

    class Meta:
        abstract = True
        unique_together = [("resource", "permission")]

    def __str__(self):
        return f"{self.pk} - {self.label} - {self.permission}"


class AbstractRole(Model):
    label = fields.CharField(max_length=50)
    admins = fields.ManyToManyField("models.Admin")
    permissions = fields.ManyToManyField("models.Permission")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.pk} - {self.label}"


class AbstractLog(Model):
    admin = fields.ForeignKeyField("models.Admin")
    ip = fields.CharField(max_length=50)
    content = fields.JSONField()
    resource = fields.CharField(max_length=50)
    action = fields.CharField(max_length=50, default=enums.Action.create.value)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True
