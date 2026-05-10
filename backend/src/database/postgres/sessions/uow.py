from contextlib import asynccontextmanager

from database.postgres.sessions.session import get_async_session


class UnitOfWork:
    def __init__(self, session):
        self.session = session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()


@asynccontextmanager
async def unit_of_work():
    async for session in get_async_session():
        uow = UnitOfWork(session)
        try:
            yield uow
            await uow.commit()
        except Exception:
            await uow.rollback()
            raise
        finally:
            await uow.close()
