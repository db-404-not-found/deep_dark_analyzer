FROM python:3.11-slim

RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false

WORKDIR /backend
COPY ./pyproject.toml ./poetry.lock /backend/

RUN poetry export -f requirements.txt --output /backend/requirements.txt \
    --without-hashes --without-urls \
    && pip install -r /backend/requirements.txt

COPY ./backend/ /backend/backend