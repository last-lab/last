import os

from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_USERNAME = "long2ice"

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_RECAPTCHA_SITE_KEY = os.getenv("GOOGLE_RECAPTCHA_SITE_KEY", "")
GOOGLE_RECAPTCHA_SECRET = os.getenv("GOOGLE_RECAPTCHA_SECRET", "")

SSO_CLIENT_ID = os.getenv("SSO_CLIENT_ID", "")
SSO_CLIENT_SECRET = os.getenv("SSO_CLIENT_SECRET", "")
SSO_REDIRECT_URL = os.getenv(
    "SSO_REDIRECT_URL", "http://127.0.0.1:8000/admin/oauth2/sso_oauth2_provider"
)
SSO_TOKEN = os.getenv("SSO_TOKEN", "")
SSO_USERNAME = "long2ice"

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["dashboard.models", "dashboard.biz_models"],
            "default_connection": "default",
        }
    },
    "use_tz": True,
}
