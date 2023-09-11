import os

import docker

from last.config import settings
from last.services.system import app_manager, db_manager
from last.types.api_models import URI, AppVariant, Image

db_manager.print_all()
app_manager.remove_app("baby_name_generator")
# app = AppVariant(app_name="baby_name_generator", variant_name="v0")
# app_manager.remove_app_variant(app)
# app = AppVariant(app_name="baby_name_generator", variant_name="v0.2")
# app_manager.remove_app_variant(app)
