from tortoise import Model, fields

from dashboard.enums import GenderType, ProductType, Status
from last.services.models import (
    AbstractAdmin,
    AbstractLog,
    AbstractPermission,
    AbstractResource,
    AbstractRole,
)


class Admin(AbstractAdmin):
    email = fields.CharField(max_length=200, default="")
    last_login = fields.DatetimeField(description="Last Login", null=True)
    avatar = fields.CharField(max_length=200, default="")
    channel = fields.CharField(default="github", max_length=20)
    intro = fields.TextField(default="")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}#{self.username}"


class Category(Model):
    slug = fields.CharField(max_length=200)
    name = fields.CharField(max_length=200)
    created_at = fields.DatetimeField(auto_now_add=True)


class Product(Model):
    categories = fields.ManyToManyField("models.Category")
    name = fields.CharField(max_length=50)
    view_num = fields.IntField(description="View Num")
    sort = fields.IntField()
    is_reviewed = fields.BooleanField(description="Is Reviewed")
    type = fields.IntEnumField(ProductType, description="Product Type")
    image = fields.CharField(max_length=200)
    body = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)


class Config(Model):
    label = fields.CharField(max_length=200)
    key = fields.CharField(max_length=20, unique=True, description="Unique key for config")
    value = fields.JSONField()
    status: Status = fields.IntEnumField(Status, default=Status.on)


class Evaluation(Model):
    name = fields.CharField(max_length=50)


class Log(AbstractLog):
    class Meta:
        ordering = ["-id"]


class Resource(AbstractResource):
    pass


class Permission(AbstractPermission):
    pass


class Role(AbstractRole):
    pass


class Sponsor(Model):
    username = fields.CharField(max_length=50)
    amount = fields.DecimalField(max_digits=8, decimal_places=2)
    currency = fields.CharField(max_length=10, default="$")
    sponsor_date = fields.DateField()

    class Meta:
        ordering = ["-id"]


class Cat(Model):
    name = fields.CharField(max_length=200)
    age = fields.IntField()
    birth_at = fields.DatetimeField(auto_now_add=True)


class Dog1(Model):
    name = fields.CharField(max_length=50)
    age = fields.IntField(description="View Age")
    gender = fields.IntEnumField(GenderType, description="Gender Type")
    image = fields.CharField(max_length=200)
    birth_at = fields.DatetimeField(auto_now_add=True)
