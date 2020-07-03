# this is a size-optimised dockerfile for production.
# for development, please use dev.dockerfile instead

# intermediate stage to export requirements.txt from pyproject.toml
FROM python:3.8-slim AS requirements

WORKDIR /

COPY ./poetry.lock ./pyproject.toml /

SHELL ["/bin/sh", "-e", "-c"]

RUN \
pip install --no-cache-dir poetry; \
poetry export --format requirements.txt > /requirements.txt; \
chmod 444 /requirements.txt

FROM python:3.8-slim

COPY --from=requirements /requirements.txt /

WORKDIR /app

COPY . /app

RUN \
apt-get update; \
apt-get upgrade -y; \
apt-get clean; \
apt-get autoremove -y; \
PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir --upgrade pip setuptools -r /requirements.txt; \

EXPOSE 80

CMD gunicorn -k uvicorn.workers.UvicornWorker -c /app/gunicorn_config.py tome.app:app
