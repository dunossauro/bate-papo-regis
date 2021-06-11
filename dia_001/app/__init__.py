from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class UserSchema(BaseModel):
    nome: str
    idade: int
    email: str


def create_app():
    app = FastAPI()

    # Trabalharemos aqui
    # Configs
    # Plugar coisas (varios apps) - Routers
    # app.registrar_outro_router

    @app.get('/')
    def home():
        return {'message': 'Ola Regis'}

    @app.get('/pessoas/{nome}')
    def pessoas(nome: str):
        return {'message': f'Você chamou {nome}'}

    @app.get('/id/{id_}')
    def busca_por_id(id_: int):
        if id_ == 1:
            raise HTTPException(
                status_code=404, detail=f'Não tem {id_}'
            )
        return {'name': 'regis'}

    @app.post('/inserir/', status_code=201)
    def inserir_no_banco(user: UserSchema):
        return {}

    return app
