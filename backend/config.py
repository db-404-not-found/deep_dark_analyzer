from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TEST: bool = False
    DEBUG: bool = False
    VERSION: str = "0.0.1"
    DESCRIPTION: str = "CBR text analyzer"

    PROJECT_NAME: str = "404"

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    CELERY_BROKER_HOST: str = "rabbitmq"
    CELERY_BROKER_PORT: int = 5672
    CELERY_BROKER_USER: str = "guest"
    CELERY_BROKER_PASSWORD: str = "guest"

    def build_db_connection_url(
        self,
        *,
        driver: str | None = None,
        host: str | None = None,
        port: int | None = None,
        user: str | None = None,
        password: str | None = None,
        database: str | None = None,
    ) -> str:
        return "postgresql+{}://{}:{}@{}:{}/{}".format(
            driver or "asyncpg",
            user or self.POSTGRES_USER,
            password or self.POSTGRES_PASSWORD,
            host or self.POSTGRES_HOST,
            port or self.POSTGRES_PORT,
            database or self.POSTGRES_DB,
        )

    def build_celery_url(
        self,
        *,
        driver: str | None = None,
        host: str | None = None,
        port: int | None = None,
        user: str | None = None,
        password: str | None = None,
    ) -> str:
        return "{}://{}:{}@{}:{}//".format(
            driver or "amqp",
            user or self.CELERY_BROKER_USER,
            password or self.CELERY_BROKER_PASSWORD,
            host or self.CELERY_BROKER_HOST,
            port or self.CELERY_BROKER_PORT,
        )
