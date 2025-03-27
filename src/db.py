from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from .models import Base

class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_async_engine(db_url)
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def create_table(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self):
        await self.engine.dispose()

    async def insert_record(self, model_cls, data: dict):
        async with self.async_session() as session:
            try:
                session.add(model_cls(**data))
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise
            except Exception:
                await session.rollback()
                raise