import uuid
from typing import Any

from sqlalchemy import ScalarResult, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models import Task
from backend.db.repositories.base import Repository
from backend.utils import clear_text


class TaskRepository(Repository[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Task, session=session)

    async def read_by_id(self, task_id: uuid.UUID) -> Task | None:
        return await self._read_by_id(id=task_id)

    async def create(self, press_release: str) -> Task:
        press_release = clear_text(press_release)
        stmt = insert(Task).values(press_release=press_release).returning(Task)
        result: ScalarResult[Task] = await self._session.scalars(
            select(Task).from_statement(stmt)
        )
        await self._session.commit()
        task = result.first()
        if task is None:
            raise Exception
        return task

    async def read_task_by_press_release(self, press_release: str) -> Task | None:
        press_release = clear_text(press_release)
        return (
            await self._session.scalars(
                select(Task).filter_by(press_release=press_release)
            )
        ).first()

    async def update(self, *args: Any, **kwargs: Any) -> Task | None:
        return await self._update(*args, **kwargs)

    async def increment_counter(
        self, task_id: uuid.UUID, cur_value: int
    ) -> Task | None:
        return await self.update(Task.id == task_id, counter=cur_value + 1)
