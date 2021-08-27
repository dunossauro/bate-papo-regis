"""
- Application Factory

Documentação dos testes: https://fastapi.tiangolo.com/tutorial/testing/?h=testing
requests do client: https://docs.python-requests.org/en/master/
"""
from app import create_app
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture


@fixture
def client():
    """Cliente do fastAPI. """
    app = create_app()
    return TestClient(app)


def test_create_app():
    assert isinstance(create_app(), FastAPI)


def test_home_deve_retornar_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_home_deve_retornar_ola_regis(client):
    response = client.get('/')
    assert response.json() == {'message': 'Ola Regis'}


def test_pessoas_deve_retornar_200_quando_chamar_com_eduardo(client):
    response = client.get('/pessoas/eduardo')
    # assert response.json() == {'message': 'Você chamou eduardo'}
    assert response.status_code == 200


def test_pessoas_deve_retornar_chamou_eduardo_quando_chamar_com_eduardo(
        client
):
    response = client.get('/pessoas/eduardo')
    assert response.json() == {'message': 'Você chamou eduardo'}


def test_busca_por_id_1_deve_retornar_404(client):
    response = client.get('/id/1')
    assert response.status_code == 404


def test_busca_por_id_1_deve_retornar_nao_tem_1(client):
    response = client.get('/id/1')
    assert response.json() == {'detail': 'Não tem 1'}


def test_busca_por_id_2_deve_retornar_200(client):
    response = client.get('/id/2')
    assert response.status_code == 200


def test_busca_por_id_2_deve_retornar_regis(client):
    response = client.get('/id/2')
    assert response.json() == {'name': 'regis'}


def test_inserir_usuario_no_banco_deve_retornar_201(client):
    user = {
        'nome': 'Regis',
        'idade': 42,
        'email': '@@'
    }
    response = client.post('/inserir/', json=user)
    assert response.status_code == 201


def test_inserir_entidade_não_processável_retorna_422(client):
    user = {
        'nome': 'Regis',
        'email': '@@'
    }
    response = client.post('/inserir/', json=user)
    print(response.json())
    assert response.status_code == 422
