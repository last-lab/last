from starlette.requests import Request

from examples.models import Category
from fastapi_admin.providers.import_export import Field, ImportExportResource


class SlugField(Field):
    async def get_export_value(self, request: Request, values: dict):
        value = await super(SlugField, self).get_export_value(request, values)
        return value.title()

    async def get_import_value(self, request: Request, values: dict):
        value = await super(SlugField, self).get_import_value(request, values)
        return value.lower()


class CategoryImportExport(ImportExportResource):
    model = Category
    fields = [SlugField(field_name="slug", title_name="SLUG"), "name"]
