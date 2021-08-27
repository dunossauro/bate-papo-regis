from os import getenv
from typing import Literal, Union

from pydantic import (
    BaseSettings,
    Field,
    PostgresDsn,
    ValidationError,
    parse_obj_as
)


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
except ValidationError:
    raise ValueError('Ambiente de Produção precisa do POSTGRES_URL')
