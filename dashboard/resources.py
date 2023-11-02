from datetime import date
from pathlib import Path
from typing import List

from starlette.requests import Request

from dashboard import enums
from dashboard.biz_models import AuditPage  # EvaluationPlan,; Evaluation,
from dashboard.biz_models import EvaluationPlan  # EvaluationPlan,; Evaluation,
from dashboard.biz_models import DataSet, LabelPage, TaskManage
from dashboard.biz_models.eval_model import Record
from dashboard.constants import BASE_DIR
from dashboard.models import Admin, Log  # EvaluationPlan,; Evaluation,
from dashboard.models import Permission as PermissionModel
from dashboard.models import Resource as ResourceModel
from dashboard.models import Role as RoleModel
from dashboard.widgets.displays import (  # ShowAudit,; ShowAuditProgress,
    OperationField,
    ShowAction,
    ShowAdmin,
    ShowAudit,
    ShowAuditProgress,
    ShowIp,
    ShowLabel,
    ShowLabelProgress,
    ShowPlan,
    ShowPlanDetail,
    ShowPopover,
    ShowRiskType,
    ShowSecondType,
    ShowStatus,
    ShowTaskAuditProgress,
    ShowTaskLabelingProgress,
    ShowTime,
)
from dashboard.widgets.filters import SearchFilter
from last.services import enums as _enums
from last.services.app import app
from last.services.enums import Method
from last.services.file_upload import FileUpload
from last.services.i18n import _
from last.services.resources import (
    Action,
    ComputeField,
    Dropdown,
    Field,
    Link,
    Model,
    ToolbarAction,
)
from last.services.widgets import displays, filters, inputs

upload = FileUpload(uploads_dir=f"{(Path(BASE_DIR) / 'static' / 'uploads').resolve()}")


@app.register
class Administartor(Dropdown):
    """安全监管"""

    class Dashboard(Link):
        label = _("Dashboard")
        icon = "fas fa-home"
        url = "/admin"

    class Notification(Link):
        label = _("Notification")  # Note: use i18n._() to translate
        icon = "far fa-bell"
        url = "/admin/notification"

    class RiskManage(Link):
        label = _("风险维度")
        icon = "fas fa-tag"
        url = "/admin/risk"

    label = _("Administartor")
    icon = "fas fa-bars"
    resources = [Dashboard, Notification, RiskManage]


@app.register
class Evaluation(Dropdown):
    """模型评测"""

    class Create(Link):
        """创建评测"""

        label = _("创建评测")
        icon = "fas fa-tag"
        url = "/admin/record/add"

    class Record(Model):
        """评测记录"""

        label = _("评测记录")
        model = Record

        filters = [
            filters.Search(
                name="llm_name",
                label="Search",
                search_mode="contains",
                placeholder="评测模型/版本/方案",
            ),
            filters.Enum(enum=enums.EvalStatus, name="state", label="评测状态"),
        ]
        fields = [
            Field(name="llm_name", label="评测模型", display=ShowPopover()),
            Field(name="plan_id", label="评测方案", display=ShowPlanDetail()),
            Field(name="created_at", label="提交时间", display=ShowTime()),
            Field(name="state", label="评测状态", display=ShowStatus()),
            OperationField(name="llm_id", label="操作"),
        ]

        async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
            return [
                ToolbarAction(
                    label=_("create"),
                    icon="fas fa-plus",
                    name="add",
                    method=Method.GET,
                    ajax=False,
                    class_="btn-dark",
                )
            ]

        async def get_actions(self, request: Request) -> List[Action]:
            return []

    label = _("模型评测")
    icon = "fas fa-user"
    resources = [Record, Create]


@app.register
class DataManager(Dropdown):
    class EvaluationPlanResource(Model):
        label = _("评测方案管理")
        model = EvaluationPlan
        filters = [filters.Search(name="name", label="方案名称", placeholder="请输入")]
        fields = [
            "id",
            Field(name="name", label="评测方案"),
            Field(name="dimensions", label="风险类型/数据占比/评测权重"),
            Field(name="dataset_ids", label="风险类型/数据占比/评测权重", display=displays.InputOnly()),
            Field(
                name="eval_type",
                label="评分方式",
                display=displays.InputOnly(),
                input_=inputs.RadioEnum(
                    enums.EvaluationType, default=enums.EvaluationType.auto_ai_critique
                ),
            ),
            Field(name="name", label="操作", display=ShowPlan()),
        ]

        async def get_actions(self, request: Request) -> List[Action]:
            return [
                # Action(
                #     label=_("update"),
                #     icon="ti ti-edit",
                #     name="epm_update",
                #     method=_enums.Method.GET,
                #     ajax=False,
                # ),
                # Action(
                #     label=_("复制并新建"),
                #     icon="ti ti-toggle-left",
                #     name="epm_copy_create",
                #     method=_enums.Method.GET,
                #     ajax=False,
                # ),
                # Action(
                #     label=_("delete"),
                #     icon="ti ti-trash",
                #     name="delete",
                #     method=_enums.Method.DELETE,
                # ),
            ]

        async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
            return [
                ToolbarAction(
                    label=_("新建方案"),
                    icon="fas fa-plus",
                    name="epm_create",
                    method=_enums.Method.GET,
                    ajax=False,
                    class_="btn-dark",
                )
            ]

    class DatasetResource(Model):
        label = _("评测集管理")
        model = DataSet
        page_title = _("评测集管理")
        filters = [
            filters.Search(name="name", label="评测集名称", search_mode="contains", placeholder="请输入"),
            SearchFilter(name="first_risk_id", label="风险类型", placeholder="请输入"),
        ]
        fields = [
            Field(name="name", label="评测集名称"),
            Field(name="focused_risks", label="风险类型", display=ShowRiskType()),
            Field(name="focused_risks", label="二级类型", display=ShowSecondType()),
            Field(name="updated_at", label="更新时间"),
            Field(name="used_by", label="使用次数"),
            Field(name="uid", label="操作", display=ShowAction()),
        ]

        async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
            return [
                ToolbarAction(
                    label=_("上传评测集"),
                    icon="fas fa-upload",
                    name="upload_dataset",
                    method=_enums.Method.GET,
                    ajax=False,
                    class_="btn-primary",
                )
            ]

        async def get_actions(self, request: Request) -> List[Action]:
            return []

    label = _("datamanager")
    icon = "fas fa-bars"
    resources = [DatasetResource, EvaluationPlanResource]


@app.register
class LogResource(Model):
    label = _("Log")
    model = Log
    icon = "far fa-sticky-note"
    fields = [
        "id",
        "admin",
        Field(name="ip", label="IP", display=ShowIp()),
        "resource",
        "content",
        "action",
        "created_at",
    ]
    filters = [
        filters.ForeignKey(
            name="admin",
            label="Admin",
            model=Admin,
        ),
        filters.DistinctColumn(
            Log,
            name="action",
            label="Action",
        ),
        filters.Date(name="created_at", label="CreatedAt"),
    ]

    async def get_toolbar_actions(self, request: Request) -> List[Action]:
        return []

    async def column_attributes(self, request: Request, field: Field) -> dict:
        if field.name == "content":
            return {"width": "40%"}
        return await super().column_attributes(request, field)

    async def cell_attributes(self, request: Request, obj: dict, field: Field) -> dict:
        if field.name == "id":
            return {"class": "bg-danger text-white"}
        return await super().cell_attributes(request, obj, field)

    async def get_actions(self, request: Request) -> List[Action]:
        return []

    async def get_bulk_actions(self, request: Request) -> List[Action]:
        return []


@app.register
class Auth(Dropdown):
    class AdminResource(Model):
        label = _("Admin")
        model = Admin
        icon = "fas fa-user"
        page_pre_title = "admin list"
        page_title = "Admin Model"
        filters = [
            filters.Search(
                name="username",
                label="Name",
                search_mode="contains",
                placeholder="Search for username",
            ),
            filters.Date(name="created_at", label="CreatedAt", placeholder="Filter by created_at"),
            filters.Boolean(name="is_active", label="IsActive"),
        ]
        fields = [
            "id",
            "username",
            "channel",
            Field(
                name="password",
                label="Password",
                display=displays.InputOnly(),
                input_=inputs.Password(help_text="Password will auto hash when changed"),
            ),
            Field(name="email", label="Email", input_=inputs.Email()),
            Field(
                name="avatar",
                label="Avatar",
                display=displays.Image(width="40"),
                input_=inputs.Image(null=True, upload=upload),
            ),
            "last_login",
            "is_superuser",
            "is_active",
            "created_at",
            Field(name="username", label="操作", display=ShowAdmin()),
        ]

        async def get_actions(self, request: Request) -> List[Action]:
            return []

    class Resource(Model):
        label = _("Resource")
        model = ResourceModel

        async def get_actions(self, request: Request) -> List[Action]:
            return []

        async def get_bulk_actions(self, request: Request) -> List[Action]:
            return []

    class Permission(Model):
        label = _("Permission")
        model = PermissionModel

        async def get_actions(self, request: Request) -> List[Action]:
            return []

        async def get_bulk_actions(self, request: Request) -> List[Action]:
            return []

    class Role(Model):
        label = _("Role")
        model = RoleModel

    label = _("Auth")
    icon = "fas fa-users"
    resources = [AdminResource, Resource, Permission, Role]


class RestDays(ComputeField):
    async def get_value(self, request: Request, obj: dict):
        v = await super(RestDays, self).get_value(request, obj)
        days = (v - date.today()).days
        return days if days >= 0 else 0


class Amount(ComputeField):
    async def get_value(self, request: Request, obj: dict):
        v = await super(Amount, self).get_value(request, obj)
        return f'{obj.get("currency")}{v}'


@app.register
class SwitchLayout(Link):
    label = _("Switch Layout")
    url = "/admin/layout"
    icon = "fas fa-grip-horizontal"


@app.register
class TaskManagePanel(Dropdown):
    """ """

    class CreateTask(Model):
        label = _("任务看板")
        model = TaskManage
        filters = [filters.Search(name="task_type", label="Task Type")]
        fields = [
            "id",
            "task_id",
            "labeling_method",
            "dateset",
            "create_time",
            "current_status",
            Field(name="task_id", label="标注进展", display=ShowTaskLabelingProgress()),
            Field(name="task_id", label="审核进展", display=ShowTaskAuditProgress()),
        ]

        async def get_actions(self, request: Request) -> List[Action]:
            return [
                Action(
                    label=_("下载标注结果"),
                    icon="ti ti-edit",
                    name="download",
                    method=Method.GET,
                    ajax=False,
                ),
            ]

        async def get_bulk_actions(self, request: Request) -> List[Action]:
            return []

        async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
            return [
                ToolbarAction(
                    label=_("创建标注任务"),
                    icon="fas fa-upload",
                    name="create_task",
                    method=_enums.Method.GET,
                    ajax=False,
                    class_="btn-primary",
                ),
                ToolbarAction(
                    label=_("上传已标注数据"),
                    icon="fas fa-upload",
                    name="upload_labeled_data",
                    method=_enums.Method.POST,
                    class_="btn-primary",
                ),
            ]

    class LabelingRecord(Model):
        label = _("Labeling Record")
        model = LabelPage
        filters = [filters.Search(name="task_type", label="Task Type")]
        fields = [
            "id",
            "task_id",
            "task_type",
            "labeling_method",
            "end_time",
            Field(name="task_id", label="标注进展", display=ShowLabelProgress()),
            Field(name="task_id", label="操作", display=ShowLabel()),
        ]

        async def get_actions(self, request: Request) -> List[Action]:
            return []

        async def get_bulk_actions(self, request: Request) -> List[Action]:
            return []

        async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
            return []

    class AuditRecord(Model):
        label = _("Audit Record")
        model = AuditPage
        filters = [filters.Search(name="task_id", label="任务id")]
        fields = [
            "id",
            "task_id",
            "labeling_method",
            "end_time",
            Field(name="task_id", label="审核进展", display=ShowAuditProgress()),
            Field(name="task_id", label="操作", display=ShowAudit()),
        ]

        async def get_actions(self, request: Request) -> List[Action]:
            return []

        async def get_bulk_actions(self, request: Request) -> List[Action]:
            return []

        async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
            return []

    label = _("任务管理")
    icon = "fas fa-bars"
    resources = [CreateTask, LabelingRecord, AuditRecord]


# @app.register
# class AuditTaskPanel(Dropdown):
#     """ """

#     class CreateTask(Model):
#         label = _("任务看板")
#         model = AuditModel
#         filters = [filters.Search(name="task_type", label="Task Type")]
#         fields = ["id", "task_id", "labeling_method", "dateset", "create_time", "current_status"]

#         async def get_actions(self, request: Request) -> List[Action]:
#             return [
#                 Action(
#                     label=_("下载标注结果"),
#                     icon="ti ti-edit",
#                     name="download",
#                     method=Method.GET,
#                     ajax=False,
#                 ),
#             ]

#         async def get_bulk_actions(self, request: Request) -> List[Action]:
#             return []

#         async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
#             return [
#                 ToolbarAction(
#                     label=_("创建标注任务"),
#                     icon="fas fa-upload",
#                     name="create_task",
#                     method=_enums.Method.GET,
#                     ajax=False,
#                     class_="btn-primary",
#                 ),
#                 ToolbarAction(
#                     label=_("分配评测任务"),
#                     icon="fas fa-upload",
#                     name="assign_test_task",
#                     method=_enums.Method.POST,
#                     class_="btn-primary",
#                 ),
#             ]

#     label = _("任务管理")
#     icon = "fas fa-bars"
#     resources = [CreateTask]
