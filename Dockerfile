FROM python:3.9 as builder
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN mkdir -p /last
WORKDIR /last
COPY pyproject.toml poetry.lock /last/
ENV POETRY_VIRTUALENVS_CREATE false
RUN pip install --upgrade pip && pip3 install poetry && poetry install --no-root
COPY . /last
RUN poetry install && make compile

FROM python:3.9-slim
WORKDIR /last
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /last /last
RUN mkdir -p /last/dashboard/static
