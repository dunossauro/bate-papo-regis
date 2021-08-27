from pydantic import (
    BaseSettings,
    PostgresDsn,
    parse_obj_as,
    ValidationError,
    Field,
)
from typing import Union, Literal
from os import getenv


class Base(BaseSettings):

    class Config:
        env_file = '.env'


class Testing(Base):
    env: Literal['test']
    database_url: str = 'sqlite+aiosqlite:///./db.db'


class Production(Base):
    env: Literal['prod']
    database_url: PostgresDsn = Field(..., env='POSTGRES_URL')


class Development(Base):
    env: Literal['dev']
    database_url: PostgresDsn = Field(
        default='postgresql://postgres:postgres@localhost:5432/postgres',
    )


Context = Union[Testing, Production, Development]


try:
    env = parse_obj_as(Context, {'env': getenv('ENV', 'prod')})
    print(env)

except ValidationError as e:
    print(e)
