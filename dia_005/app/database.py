# Core
# ORM <-

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import (
    declarative_base, sessionmaker
)
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine
)

from config import env

engine = create_async_engine(env.database_url)
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
