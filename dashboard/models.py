from tortoise import Model, fields

from dashboard.enums import (
    EvalStatus,
    EvaluationType,
    GenderType,
    ProductType,
    Status,
)
from last.services.models import (
    AbstractAdmin,
    AbstractLog,
    AbstractPermission,
    AbstractResource,
    AbstractRole,
)


# 这个类里面的东西是专门用来display的
class ModelInfo(Model):
    name = fields.CharField(max_length=200, null=True)
    model_type = fields.CharField(max_length=200, null=True)
    version = fields.CharField(max_length=200, null=True)
    base_model = fields.CharField(max_length=200, null=True)
    parameter_volume = fields.CharField(max_length=200, null=True)
    pretraining_info = fields.CharField(max_length=200, null=True)
    finetuning_info = fields.CharField(max_length=200, null=True)
    alignment_info = fields.CharField(max_length=200, null=True)
    endpoint = fields.CharField(max_length=200, null=True)
    access_key = fields.CharField(max_length=200, null=True)
    secret_key = fields.CharField(max_length=200, null=True)


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


class Record(Model):
    eval_models = fields.CharField(max_length=200, null=True)
    llm_name = fields.CharField(max_length=200, null=True)
    llm_id = fields.IntField(null=True)
    eval_plan = fields.CharField(description="Choose evaluation plan", max_length=200, null=True)
    plan_id = fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    state: EvalStatus = fields.IntEnumField(EvalStatus, default=EvalStatus.on_progress, null=True)
    report = fields.BinaryField(null=True)


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


class EvaluationPlan(Model):
    """
    评测方案管理model
    """

    name = fields.CharField(max_length=200)
    eval_type = fields.IntEnumField(
        EvaluationType, description="Eval Type", default=EvaluationType.auto_ai_critique
    )
    dimensions = fields.CharField(max_length=500)
    dataset_ids = fields.CharField(max_length=200)
    current_dataset_index = fields.CharField(max_length=200, null=True)
    current_dataset_iter = fields.CharField(max_length=200, null=True)
    uid = fields.CharField(max_length=200, null=True)
    description = fields.CharField(max_length=200, null=True)
    creator = fields.CharField(max_length=200, null=True)
    editor = fields.CharField(max_length=200, null=True)
    reviewer = fields.CharField(max_length=200, null=True)
    permissions = fields.CharField(max_length=200, null=True)
    created_at = fields.DatetimeField(null=True)
    updated_at = fields.DatetimeField(null=True)


class DataSet(Model):
    # name = fields.CharField(max_length=200)
    # type = fields.CharField(max_length=200, null=True)
    # sub_type = fields.CharField(max_length=200)
    # third_type = fields.CharField(max_length=200)
    # updateTime = fields.CharField(max_length=200)
    # useCount = fields.IntField()
    name = fields.CharField(max_length=200)
    dimensions = fields.CharField(max_length=200, null=True)
    url = fields.CharField(max_length=200, null=True)
    file = fields.CharField(max_length=200, null=True)
    volume = fields.CharField(max_length=200, null=True)
    used_by = fields.CharField(max_length=200, null=True)
    qa_records = fields.CharField(max_length=200, null=True)
    conversation_start_id = fields.CharField(max_length=200, null=True)
    current_conversation_index = fields.IntField(null=True)
    current_qa_record_id = fields.IntField(null=True)


class LabelPage(Model):
    task_type = fields.CharField(max_length=50)
    labeling_method = fields.CharField(max_length=255)
    release_time = fields.DatetimeField()
    current_status = fields.CharField(max_length=50)
