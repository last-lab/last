checkfiles = last/services tests/ dashboard/ conftest.py
black_opts = -l 100 -t py38
py_warn = PYTHONDEVMODE=1
locales = last/services/locales

up:
	@poetry update

deps:
	@poetry install -E s3 -E oss

style: deps
	poetry run isort -src $(checkfiles)
	poetry run black $(black_opts) $(checkfiles)

check: deps
	poetry run black --check $(black_opts) $(checkfiles) || (echo "Please run 'make style' to auto-fix style issues" && false)
	poetry run flake8 $(checkfiles)
	# TODO: Add more strict type checking
	# mypy $(checkfiles)
	# pylint $(checkfiles)

test: deps
	$(py_warn) poetry run pytest --cov

build: deps
	@poetry build

ci: check test

# i18n
extract:
	@pybabel extract -F babel.cfg -o $(locales)/messages.pot ./

update:
	@pybabel update -d $(locales) -i $(locales)/messages.pot

compile:
	@pybabel compile -d $(locales)

babel: extract update
