from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.repositories.task import TaskRepository


class DatabaseHolder:
    def __init__(self, session: AsyncSession):
        self.task = TaskRepository(session=session)
