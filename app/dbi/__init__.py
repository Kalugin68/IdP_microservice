from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from config import env


class Database:
    def __init__(self, dsn: str):
        self.engine = create_async_engine(
            str(dsn),
            pool_pre_ping=True,
            pool_timeout=30,
            echo=False,
            pool_size=10,
            max_overflow=20
        )

    async def fetch(self, query: str, **kwargs):
        async with self.engine.connect() as conn:
            result = await conn.execute(text(query), kwargs)
            return result.fetchall()

    async def fetchrow(self, query: str, **kwargs):
        async with self.engine.connect() as conn:
            result = await conn.execute(text(query), kwargs)
            return result.first()

    async def execute(self, query: str, **kwargs):
        async with self.engine.begin() as conn:
            result = await conn.execute(text(query), kwargs)
            return result

db = Database(env.db_dsn)