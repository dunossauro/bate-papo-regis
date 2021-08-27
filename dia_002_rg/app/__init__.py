from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class UserSchema(BaseModel):
    nome: str
    email: str


class UserSchemaResponse(UserSchema):
    id: int

    class Config:
        orm_mode = True


class BatatinhaResponse(BaseModel):
    xpto: list[UserSchemaResponse]


def create_app():
    # Application factory
    app = FastAPI()

    from sqlalchemy.future import select

    from .database import User, session

    @app.get('/user/', response_model=BatatinhaResponse, status_code=200)
    async def user_list():
        async with session() as s:
            query = await s.execute(select(User))
            result = query.scalars().all()
        return {'xpto': result}

    @app.get('/user/{user_id}/', response_model=UserSchemaResponse, status_code=200)
    async def get_user(user_id):
        async with session() as s:
            query = await s.execute(
                select(User).where(User.id == user_id)
            )

            # scalar é um objeto do ORM (SQLAlchemy)
            # retorna um registro
            result = query.scalar()

        if not result:
            raise HTTPException(
                status_code=404, detail=f'Not Found {user_id}'
            )

        return result

    @app.post('/user/add/', status_code=201)
    async def create_user(user: UserSchema):
        async with session() as s:
            # Todas as operações do banco vão rolar aqui!
            s.add(
                User(nome=user.nome, email=user.email)
            )
            await s.commit()

        return user

    @app.patch('/user/{user_id}/', status_code=200)
    async def patch_user(user: UserSchema, user_id):
        async with session() as s:
            query = await s.execute(
                select(User).where(User.id == user_id)
            )

            result = query.scalar()

            if result:
                result.nome = user.nome
                result.email = user.email
                await s.commit()

        if not result:
            raise HTTPException(
                status_code=404, detail=f'Not Found {user_id}'
            )

        return {'message': str(result)}

    @app.delete('/user/{user_id}/', status_code=204)
    async def user_delete(user_id):
        async with session() as s:
            query = await s.execute(
                select(User).where(User.id == user_id)
            )

            # scalar é um objeto do ORM (SQLAlchemy)
            # retorna um registro
            result = query.scalar()

            if not result:
                raise HTTPException(
                    status_code=404, detail=f'Not Found {user_id}'
                )
            await s.delete(result)
            await s.commit()

        return {'message': 'deletado com sucesso'}

    return app
