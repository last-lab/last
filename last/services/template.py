import datetime
import os
from datetime import date
from typing import Any
from urllib.parse import urlencode

import pendulum
from jinja2 import pass_context

# from starlette.requests import Request
from starlette.templating import Jinja2Templates

from last.services import VERSION
from last.services.constants import BASE_DIR

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
templates.env.globals["VERSION"] = VERSION
templates.env.globals["NOW_YEAR"] = date.today().year
templates.env.add_extension("jinja2.ext.i18n")


@pass_context
def current_page_with_params(context: dict, params: dict):
    request = context.get("request")  # type:Request
    full_path = request.scope["raw_path"].decode()
    query_params = dict(request.query_params)
    for k, v in params.items():
        query_params[k] = v
    return full_path + "?" + urlencode(query_params)


def diff_for_humans(time: datetime.datetime):
    return (
        pendulum.now().subtract(seconds=(pendulum.now() - time).total_seconds()).diff_for_humans()
    )


templates.env.filters["current_page_with_params"] = current_page_with_params
templates.env.filters["diff_for_humans"] = diff_for_humans


def set_global_env(name: str, value: Any):
    templates.env.globals[name] = value


def get_global_env(name: str):
    return templates.env.globals.get(name)


def add_template_folder(*folders: str):
    for folder in folders:
        templates.env.loader.searchpath.insert(0, folder)
