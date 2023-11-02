# LAST

LLM Alignment and Safety Toolkit

## Installation

```bash
not supported yet
```

## Usage

```bash
not supported yet
```

## Pre-requisites

1. [Optinal] Install [conda](https://docs.conda.io/en/latest/miniconda.html) if you want to keep your system clean. 
Then create a conda environment.

```bash
conda create -n last python=3.8
conda activate last
```
2. Install [poetry](https://python-poetry.org/docs/#installation)

3. Install [redis](https://redis.io/topics/quickstart)

## Run dashboard in local
create a .env file in the root directory of the project and add the following variables
```bash
DATABASE_URL=sqlite://dashboard/app.sqlite3
REDIS_URL=redis://localhost:6379/0
```
then go to the project directory and run the following commands
```bash
poetry install && make compile
poetry run python dashboard/main.py
```
If this is the first time you run the dashboard, you need to create an admin user 
by visiting http://127.0.0.1:8000/admin/init

For more detail, checkout Dockfile and docker-compose.yml in case I miss something.

如果遇到redis服务出错的情况，使用 sudo /etc/init.d/redis-server restart 命令重启redis

# Locales
当需要使用中文时，使用`from last.services.i18n import _`代替`_`，并在需要翻译的字符串前加上`_`，例如：
```python
from last.services.i18n import _
label = _('label')
```
之后，使用`make babel`提取需要翻译的字符串，文件存储在`last/services/locales/zh_CN/LC_MESSAGES/messages.po`。
修改完成后，使用`make compile`编译翻译文件。