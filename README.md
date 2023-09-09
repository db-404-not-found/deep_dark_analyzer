# Deep Dark Analyzer

## Description

<a href="https://github.com/Ileriayo/markdown-badges">
  <p align="center">
    <img alt="React" src="https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB" />
    <img alt="React Query" src="https://img.shields.io/badge/-React%20Query-FF4154?style=for-the-badge&logo=react%20query&logoColor=white" />
    <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
    <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi"/>
    <img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"/>
    <img alt="Postgres" src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white"/>
    <img alt="Nginx" src="https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white"/>
    <img alt="GitHub" src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/>
    <img alt="RabbitMQ" src="https://img.shields.io/badge/Rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white"/>
  </p>
</a>

## Installation

For work with the project you need to download source code from this repo:

```bash
git clone https://github.com/db-404-not-found/deep_dark_analyzer
```

## Configuration

For configuration the project you should setup env variables in your workspace or create
copy of  `.env.dev` file with actual environment variables values.

If you plan to use postgres database not from `docker-compose.yaml` note to change
`POSTGRES_HOST` and `POSTGRES_PORT` vars.

```bash
cp .env.dev .env
```

```bash
POSTGRES_USER      # user for connection to database
POSTGRES_PASSWORD  # user password for connection to database
POSTGRES_HOST      # IP-address or domain of database server
POSTGRES_PORT      # port of database server
POSTGRES_DB        # database name
```

## Running

### Docker

To run the entire project use Docker Compose file.

```bash
docker compose up --build -d
```

### Locally

Requirements: target python version - **3.11**

For running project locally you need to use `poetry`

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip poetry
poetry install --no-root
set -a
source .env
set +a
poetry run gunicorn -c backend/gunicorn.conf.py backend.main:app
```

After executing commands above you can open browser on
[http://127.0.0.1:8000/docs/swagger](http://127.0.0.1:8000/docs/swagger) for use
Swagger with our API.

### Database migration

After running you need to update database with migrations:

If locally

```bash
alembic -c ./backend/alembic.ini upgrade head
```

If docker

```bash
docker compose exec backend alembic -c backend/alembic.ini upgrade head
```

To create new migration with autointrospection use these commands:

```bash
alembic -c ./backend/alembic.ini revision --autogenerate -m "New migration name"
```

or

```bash
docker compose exec backend alembic -c backend/alembic.ini revision --autogenerate -m "New migration name"
```

## Using

After running full project in docker you can open landing on `http://127.0.0.1/` with
form for analyze press release.

- `GET  /api/v1/monitoring/ping` - healthchecking server
- `POST /api/v1/tasks/` - create new task to analyze press release text to get inference
- `GET  /api/v1/tasks/{task_id}` - get result of analyzing press release