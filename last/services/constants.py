import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# time format of pendulum
DATETIME_FORMAT = "DD MMMM YYYY HH:mm:ss A"
DATE_FORMAT = "DD MMMM YYYY"

DATETIME_FORMAT_MOMENT = "YYYY-MM-DD HH:mm:ss"
DATE_FORMAT_MOMENT = "YYYY-MM-DD"

# redis cache
CAPTCHA_ID = "captcha:{captcha_id}"
LOGIN_ERROR_TIMES = "login_error_times:{ip}"
LOGIN_USER = "login_user:{token}"

# login
ACCESS_TOKEN = "access_token"
LOGIN_EXPIRE = 3600 * 24 * 30
