FROM python:3.11-slim-bullseye as base

RUN apt-get update -y && apt-get install -y gcc
# RUN apt-get install -y build-essential libssl-dev libffi-dev python-dev

FROM base as builder

WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR  /

COPY poetry.lock pyproject.toml README.md ./
COPY src/ src/.
COPY tests/ tests/.

RUN ls
RUN poetry install

FROM builder as stage

RUN poetry run pytest tests/

FROM stage as runtime

RUN poetry run python -m world_peace