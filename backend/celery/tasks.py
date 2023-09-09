from uuid import UUID

from celery import Celery
from loguru import logger
from sqlalchemy.orm import Session

from backend.celery.base import DatabaseTask
from backend.celery.inference import MultiFunctionalModel
from backend.config import Settings
from backend.db.models import Status, Task

settings = Settings()

celery = Celery(
    "worker",
    broker=settings.build_celery_url(),
    backend="rpc://",
)


@celery.task(base=DatabaseTask, name="inference_task", bind=True, track_started=True)
def make_inference(self: DatabaseTask, task_id: UUID) -> None:
    logger.info("Started task {task_id}", task_id=task_id)
    with Session(self.engine) as session:
        process_task(session=session, task_id=task_id, model=self.model)
    logger.info("Task {task_id} was ended", task_id=task_id)
    return


def process_task(session: Session, task_id: UUID, model: MultiFunctionalModel) -> None:
    task = session.get(Task, task_id)
    if task is None:
        logger.error("Task not found")
        return
    task.status = Status.STARTED
    session.commit()
    session.refresh(task)
    task.result = model.predict(task.press_release)
    task.status = Status.RESPONSED
    session.commit()
    return
