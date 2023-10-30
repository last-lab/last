import typing
from typing import List

from fastapi import Depends
from starlette.requests import Request

from last.services.depends import get_resources
from last.services.providers import Provider
from last.services.template import templates

if typing.TYPE_CHECKING:
    from last.services.app import FastAPIAdmin


class SearchProvider(Provider):
    name = "search_provider"

    def __init__(self, path: str = "/search"):
        self.path = path

    async def register(self, app: "FastAPIAdmin"):
        await super(SearchProvider, self).register(app)
        app.get(self.path)(self.search_page)

    def _resolve_resources(
        self, results: list, request: Request, resources: List[dict], search_text: str
    ):
        for r in resources:
            label = r.get("label")
            type_ = r.get("type")
            if search_text.lower() in label.lower():
                if type_ == "link":
                    results.append(dict(label=label, url=r.get("url")))
                elif type_ == "model":
                    results.append(
                        dict(
                            label=label,
                            url=request.app.admin_path + "/" + r.get("model") + "/list",
                        )
                    )
            if type_ == "dropdown":
                self._resolve_resources(
                    results, request, r.get("resources"), search_text
                )

    async def search_page(
        self,
        request: Request,
        search_text: str,
        resources: List[dict] = Depends(get_resources),
    ):
        if search_text:
            results = []
            self._resolve_resources(results, request, resources, search_text)
            return templates.TemplateResponse(
                "providers/search/search_result.html",
                context={
                    "request": request,
                    "results": results,
                    "search_text": search_text,
                },
            )
