"""
- Application Factory

Documentação dos testes: https://fastapi.tiangolo.com/tutorial/testing/?h=testing
requests do client: https://docs.python-requests.org/en/master/
"""
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app import create_app
from app.database import Base, User


@fixture
def client():
    """Cliente do FastAPI. """
    app = create_app()

    # Conexão sincrona no banco para criar as tabelas
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///./db_test.db')

    with engine.begin() as conn:
        Base.metadata.create_all(conn)

        yield TestClient(app)  # cliente do FastAPI

        Base.metadata.drop_all(conn)


@fixture
def engine():
    from sqlalchemy import create_engine
    return create_engine('sqlite:///./db_test.db')


@fixture
def user():
    return {
        'nome': 'Regis',
        'email': '@@'
    }


@fixture
def userid():
    return {
        'id': 1,
        'nome': 'Regis',
        'email': '@@'
    }


def test_create_user_deve_retornar_201(client, user):
    response = client.post('/user/add/', json=user)
    assert response.status_code == 201


def test_create_user_deve_retornar_o_usuario_de_entrada(client, user):
    response = client.post('/user/add/', json=user)
    assert response.json() == user


def test_patch_user_deve_retornar_404_quando_usuario_nao_existir(client, user):
    response = client.patch('/user/1/', json=user)
    assert response.status_code == 404


def test_patch_user_deve_retornar_200_quando_usuario_alterar_o_user(client, user):
    response = client.post('/user/add/', json=user)

    user['email'] = 'batatinha@frita'

    response = client.patch('/user/1/', json=user)
    assert response.status_code == 200


def test_patch_user_deve_alterar_o_registro_no_banco(client, user, engine):
    # docs.sqlalchemy.org/en/14/orm/session_basics.html#basics-of-using-a-session
    client.post('/user/add/', json=user)

    user['email'] = 'batatinha@frita'

    client.patch('/user/1/', json=user)

    with Session(engine) as s:
        query = s.execute(
            select(User).where(User.id == 1)
        )
        assert query.scalar().email == 'batatinha@frita'


def test_get_user_deve_retornar_200_quando_chamar_id_1(client, user):
    client.post('/user/add/', json=user)

    response = client.get('/user/1/')
    assert response.status_code == 200


def test_get_user_deve_retornar_usuario_quando_chamar_id_1(client, user, userid):
    client.post('/user/add/', json=user)

    response = client.get('/user/1/')
    assert response.json() == userid
