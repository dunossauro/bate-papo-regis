from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from typing import List


class UserBase(BaseModel):
    nome: str
    idade: int
    email: str


class UserCreate(UserBase):
    ...


class UserSchema(UserBase):
    id: int


PESSOAS = [
    {"id": 1, "nome": "Regis", "idade": 42, "email": "regis@email.com"}
]
ID_COUNTER = 1


def create_app():
    app = FastAPI()

    # Configs
    # Plugar coisas (vários apps) - Routers
    # app.registrar_outro_router

    @app.get('/')
    def home():
        return {'message': 'Ola Regis'}

    @app.get('/pessoa/{nome}')
    def pessoa(nome: str):
        return {'message': f'Você chamou {nome}'}

    @app.get('/id/{id_}')
    def busca_por_id(id_: int):
        if id_ == 1:
            raise HTTPException(status_code=404, detail=f'Não tem {id_}')
        # return {'message': str(type(id_))}
        return {'name': 'regis'}

    @app.post('/inserir/', status_code=201)
    def inserir_no_banco(user: UserSchema):
        return {}

    @app.get('/pessoas', response_model=List[UserSchema])
    def pessoas_list():
        return PESSOAS

    @app.get('/pessoas/{id_}', response_model=UserSchema)
    def get_pessoas(id_: int):
        for pessoa in PESSOAS:
            if pessoa['id'] == id_:
                return pessoa

        raise HTTPException(status_code=404, detail='Pessoa not found.')

    @app.post('/pessoas/add/', response_model=UserSchema, status_code=201)
    def pessoas_create(pessoa: UserCreate):
        global ID_COUNTER

        nova_pessoa = pessoa.dict()
        nova_pessoa['id'] = ID_COUNTER

        ID_COUNTER += 1

        PESSOAS.append(nova_pessoa)
        return nova_pessoa

    return app
