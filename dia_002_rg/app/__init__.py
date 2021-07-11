from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class UserSchema(BaseModel):
    nome: str
    email: str


def create_app():
    # Application factory
    app = FastAPI()

    from .database import session, User
    from sqlalchemy.future import select

    @app.post('/user/add/', status_code=201)
    async def create_user(user: UserSchema):
        ...

    @app.patch('/user/{user_id}/', status_code=200)
    async def patch_user(user: UserSchema, user_id):
        ...

    return app
