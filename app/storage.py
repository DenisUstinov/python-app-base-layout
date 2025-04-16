from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from .models import Base

class Storage:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url)
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def create_table(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def insert_record(self, model_cls, data: dict):
        async with self.async_session() as session:
            try:
                session.add(model_cls(**data))
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                raise e

    async def close(self):
        await self.engine.dispose()
