# Core
# ORM <-

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import (
    declarative_base, sessionmaker
)
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine
)

engine = create_async_engine(
    'sqlite+aiosqlite:///./db.db'
)
session = sessionmaker(
    engine,
    expire_on_commit=True,
    class_=AsyncSession
)  # 1.4 +

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)


async def create_database():
    # Conecta no banco
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    from asyncio import run
    run(create_database())
