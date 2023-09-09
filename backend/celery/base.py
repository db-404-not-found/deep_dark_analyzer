from celery import Task
from sqlalchemy import create_engine

from backend.celery.inference import MultiFunctionalModel
from backend.config import Settings


class DatabaseTask(Task):
    def __init__(self) -> None:
        super().__init__()
        self.settings = Settings()
        self.engine = create_engine(
            url=self.settings.build_db_connection_url(driver="psycopg2")
        )
        self.model = MultiFunctionalModel()
