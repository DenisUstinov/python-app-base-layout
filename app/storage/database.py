from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from .models import Base

class Database:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url)
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def create_table(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def select_fields(self, model, fields: list[str] = None, filters: dict = None):
        async with self.async_session() as session:
            if fields:
                columns = [getattr(model, field) for field in fields]
                query = select(*columns)
            else:
                query = select(model)

            if filters:
                for column_name, value in filters.items():
                    column = getattr(model, column_name, None)
                    if column is None:
                        continue

                    if isinstance(value, tuple) and len(value) == 2:
                        query = query.filter(and_(column >= value[0], column <= value[1]))
                    else:
                        query = query.filter(column == value)

            result = await session.execute(query)
            return result.mappings().all()

    async def insert_record(self, model_cls, data: dict):
        async with self.async_session() as session:
            try:
                session.add(model_cls(**data))
                await session.commit()
            except IntegrityError:
                await session.rollback()
            except Exception as e:
                await session.rollback()
                raise e

    async def close(self):
        await self.engine.dispose()