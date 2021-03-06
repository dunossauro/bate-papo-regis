"""
- Application Factory

Documentação dos testes: https://fastapi.tiangolo.com/tutorial/testing/?h=testing
requests do client: https://docs.python-requests.org/en/master/
"""
from app import create_app
from app.database import Base, User
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.future import select
from sqlalchemy.orm import Session


@fixture
def client():
    """Cliente do fastAPI. """
    app = create_app()

    # Conexão sincrona no banco para criar as tabelas
    from config import env
    from sqlalchemy import create_engine
    engine = create_engine(env.database_url)

    with engine.begin() as conn:
        Base.metadata.create_all(conn)

        yield TestClient(app)  # cliente do fastAPI

        Base.metadata.drop_all(conn)


@fixture
def engine():
    from sqlalchemy import create_engine
    return create_engine('sqlite:///./db.db')


@fixture
def user():
    return {
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


def test_patch_user_deve_retornar_200_quando_usuario_alterar_o_user(
        client, user
):
    response = client.post('/user/add/', json=user)

    user['email'] = 'Batatinha@frita'

    response = client.patch('/user/1/', json=user)
    assert response.status_code == 200


def test_patch_user_deve_alterar_o_registro_no_banco(
        client, user, engine
):
    # docs.sqlalchemy.org/en/14/orm/session_basics.html#basics-of-using-a-session
    client.post('/user/add/', json=user)

    user['email'] = 'Batatinha@frita'

    client.patch('/user/1/', json=user)

    with Session(engine) as s:
        query = s.execute(
            select(User).where(User.id == 1)
        )
        assert query.scalar().email == 'Batatinha@frita'
