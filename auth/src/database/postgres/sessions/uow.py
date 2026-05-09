from contextlib import asynccontextmanager

from database.postgres.sessions.session import get_async_session
from database.postgres.sessions.redis import get_redis


class UnitOfWork:
    def __init__(self, session, redis):
        self.session = session
        self.redis = redis

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()


@asynccontextmanager
async def unit_of_work():
    async for session in get_async_session():
        redis = await get_redis()
        uow = UnitOfWork(session, redis)
        try:
            yield uow
            await uow.commit()
        except Exception:
            await uow.rollback()
            raise
        finally:
            await uow.close()
