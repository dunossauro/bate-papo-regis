"""
Injeção de dependência:
- fastapi: https://fastapi.tiangolo.com/tutorial/dependencies/
- Genérico: https://python-dependency-injector.ets-labs.org/index.html
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .database import session, User

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


class UserSchema(BaseModel):
    nome: str
    email: str


def qp(a: int, b: str = 'a'):
    """Os parâmetros passados para qp são query strings."""
    return True


async def my_session():
    async with session() as s:
        yield s


def create_app():
    # Application factory
    app = FastAPI()  # Ele vai depender da criação da create_database

    from sqlalchemy.future import select

    @app.get('/index', response_class=HTMLResponse)
    def index(request: Request):
        return templates.TemplateResponse(
            # request é obrigatório
            "index.html", {"request": request}
        )

    @app.get('/')
    def index(query_string=Depends(qp)):
        """
        Transformar em um get de user

        Testar o index:

        Regra do Query Params (qp): id ou nome
        - exemplo_1: /?id=1
        - exemplo_2: /?nome='regis'

        Se não tiver nenhum dos dois, vai retornar 422
        Se não tiver no banco, vai retornar 404 -> HTTPException
        """
        return {'message': 'ok'}

    @app.post('/user/add/', status_code=201)
    async def create_user(user: UserSchema, session=Depends(my_session)):
        """
        1. Bater no endpoint
        2. Validar Schema -> user -> 422
        3. Depends -> Session -> 422
        """
        session.add(
            User(nome=user.nome, email=user.email)
        )
        await session.commit()

        return user

    @app.patch('/user/{user_id}/', status_code=200)
    async def patch_user(user: UserSchema, user_id):
        """
        Depender de session.
        """
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

    return app
