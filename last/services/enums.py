from enum import Enum


class StrEnum(str, Enum):
    def __str__(self):
        return self.value


class Permission(StrEnum):
    create = "create"
    delete = "delete"
    update = "update"
    read = "read"


class Action(StrEnum):
    create = "create"
    delete = "delete"
    update = "update"


class Layout(StrEnum):
    layout = "layout.html"
    layout_navbar = "layout-navbar.html"


class Method(StrEnum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"
    PATCH = "PATCH"


class ExportFormat(StrEnum):
    csv = "csv"
    json = "json"
    tsv = "tsv"
    yaml = "yaml"

    @classmethod
    def media_types(cls) -> dict:
        return {
            ExportFormat.csv: "text/csv",
            ExportFormat.tsv: "text/tsv",
            ExportFormat.json: "text/json",
            ExportFormat.yaml: "text/yaml",
        }

    @property
    def media_type(self):
        return self.media_types().get(self)
