import csv
import io
import json
import typing

import yaml
from fastapi import Depends, File, Form, Path
from pydantic.json import pydantic_encoder
from starlette.requests import Request
from starlette.responses import Response
from tortoise import Model

from last.services import enums
from last.services.depends import admin_log_create, get_model, get_model_resource, get_resources
from last.services.enums import Method
from last.services.i18n import _
from last.services.providers import Provider
from last.services.resources import Model as ModelResource
from last.services.resources import ToolbarAction
from last.services.template import templates

if typing.TYPE_CHECKING:
    from last.services.app import FastAPIAdmin


class Field:
    def __init__(self, field_name: str, title_name: typing.Optional[str] = None):
        """
        Config field import and export behavior
        :param field_name: field name in db
        :param title_name: field name in file, default is same as field name
        """
        self.field_name = field_name
        self.title_name = title_name or field_name.title()

    async def get_import_value(self, request: Request, values: dict):
        return values.get(self.title_name)

    async def get_export_value(self, request: Request, values: dict):
        return values.get(self.field_name)


class ImportExportResource:
    model: typing.Type[Model]
    fields: typing.List[typing.Union[str, Field]]

    @classmethod
    async def get_content_by_format(
        cls, request: Request, values: typing.List[dict], format_: enums.ExportFormat
    ):
        buffer = io.StringIO()
        keys = values[0].keys()
        if format_ == enums.ExportFormat.csv:
            writer = csv.DictWriter(buffer, fieldnames=keys)
            writer.writeheader()
            writer.writerows(values)
        if format_ == enums.ExportFormat.tsv:
            writer = csv.DictWriter(buffer, fieldnames=keys, delimiter="\t")
            writer.writeheader()
            writer.writerows(values)
        if format_ == enums.ExportFormat.json:
            json.dump(values, buffer, default=pydantic_encoder)
        if format_ == enums.ExportFormat.yaml:
            yaml.dump(values, buffer)
        return buffer.getvalue().encode()

    @classmethod
    async def get_values_by_format(
        cls, request: Request, content: bytes, format_: enums.ExportFormat
    ):
        if format_ == enums.ExportFormat.csv:
            reader = csv.DictReader(io.StringIO(content.decode()))
            return [dict(row) for row in reader]
        if format_ == enums.ExportFormat.tsv:
            reader = csv.DictReader(io.StringIO(content.decode()), delimiter="\t")
            return [dict(row) for row in reader]
        if format_ == enums.ExportFormat.json:
            return json.loads(content.decode())
        if format_ == enums.ExportFormat.yaml:
            return yaml.safe_load(content)


class ImportExportProvider(Provider):
    name = "import_export_provider"

    def __init__(
        self,
        import_export_resources: typing.Optional[
            typing.List[typing.Type[ImportExportResource]]
        ] = None,
    ):
        self._import_export_resources = {}
        for item in import_export_resources or []:
            fields: typing.List = []
            for field in item.fields:
                if isinstance(field, str):
                    fields.append(Field(field_name=field, title_name=field))
                else:
                    fields.append(field)
                item.fields = fields
            self._import_export_resources[item.model] = item

    @property
    def import_action(self):
        return ToolbarAction(
            label=_("Import"),
            icon="fas fa-file-import",
            name="import",
            method=Method.GET,
            ajax=False,
            class_="btn-secondary",
        )

    @property
    def export_action(self):
        return ToolbarAction(
            label=_("Export"),
            icon="fas fa-file-export",
            name="export",
            method=Method.GET,
            ajax=False,
            class_="btn-indigo",
        )

    async def register(self, app: "FastAPIAdmin"):
        await super(ImportExportProvider, self).register(app)

        @app.get("/{resource}/import")
        async def import_view(
            request: Request,
            resources=Depends(get_resources),
            resource: str = Path(...),
            model_resource: ModelResource = Depends(get_model_resource),
        ):
            context = {
                "query": request.query_params,
                "request": request,
                "resource": resource,
                "resources": resources,
                "resource_label": model_resource.label,
                "model_resource": model_resource,
                "format_options": enums.ExportFormat,
            }
            return templates.TemplateResponse(
                "providers/import_export/import.html",
                context=context,
            )

        @app.post("/{resource}/import", dependencies=[Depends(admin_log_create)])
        async def import_file(
            request: Request,
            import_: bytes = File(...),
            format_: enums.ExportFormat = Form(...),
            resources=Depends(get_resources),
            resource: str = Path(...),
            model_resource: ModelResource = Depends(get_model_resource),
            model=Depends(get_model),
        ):
            values = await ImportExportResource.get_values_by_format(request, import_, format_)
            import_export_resource = self._import_export_resources.get(model)
            format_values = []
            if import_export_resource:
                for value in values:
                    item = {}
                    for field in import_export_resource.fields:
                        if isinstance(field, str):
                            field = Field(field_name=field)

                        item[field.field_name] = await field.get_import_value(request, value)
                    format_values.append(item)

            objs = [model(**value) for value in format_values]
            success = error = ""
            try:
                await model.bulk_create(objs)
                success = _("Success create %(count)s %(label)s") % dict(
                    count=len(objs), label=model_resource.label
                )
            except Exception as e:
                error = str(e)
            context = {
                "request": request,
                "resource": resource,
                "resources": resources,
                "resource_label": model_resource.label,
                "model_resource": model_resource,
                "format_options": enums.ExportFormat,
                "error": error,
                "success": success,
            }
            return templates.TemplateResponse(
                "providers/import_export/import.html",
                context=context,
            )

        @app.get("/{resource}/export")
        async def export_view(
            request: Request,
            resources=Depends(get_resources),
            resource: str = Path(...),
            model_resource: ModelResource = Depends(get_model_resource),
        ):
            context = {
                "query": request.query_params,
                "request": request,
                "resource": resource,
                "resources": resources,
                "resource_label": model_resource.label,
                "model_resource": model_resource,
                "format_options": enums.ExportFormat,
            }
            return templates.TemplateResponse(
                "providers/import_export/export.html",
                context=context,
            )

        @app.post("/{resource}/export")
        async def export(
            request: Request,
            format_: enums.ExportFormat = Form(...),
            model_resource: ModelResource = Depends(get_model_resource),
            model=Depends(get_model),
            page_size: int = 10,
            page_num: int = 1,
        ):
            qs = model.all()
            params, qs = await model_resource.resolve_query_params(
                request, dict(request.query_params), qs
            )
            if page_size:
                qs = qs.limit(page_size)
            else:
                page_size = model_resource.page_size
            qs = qs.offset((page_num - 1) * page_size)
            import_export_resource = self._import_export_resources.get(model)
            if not import_export_resource:
                fields_name = model_resource.get_fields_name()
            else:
                fields_name = map(lambda x: x.field_name, import_export_resource.fields)
            values = await qs.values(*fields_name)
            format_values = []
            if import_export_resource:
                for value in values:
                    item = {}
                    for field in import_export_resource.fields:
                        item[field.title_name] = await field.get_export_value(request, value)
                    format_values.append(item)
            content = await ImportExportResource.get_content_by_format(
                request, format_values, format_
            )
            content_disposition = f'attachment; filename="{model_resource.label}.{format_}"'
            return Response(
                content,
                media_type=format_.media_type,
                headers={"content-disposition": content_disposition},
            )
