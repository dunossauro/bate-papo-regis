'''
- Application Factory
'''
from app import create_app
from pytest import fixture
from fastapi import FastAPI
from fastapi.testclient import TestClient


@fixture
def client():
    '''Cliente do FastAPI.'''
    app = create_app()
    return TestClient(app)


def test_create_app(client):
    assert isinstance(create_app(), FastAPI)


def test_home_deve_retornar_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_home_deve_retornar_ola_regis(client):
    # response é da api do requests.
    response = client.get('/')
    assert response.json() == {'message': 'Ola Regis'}


def test_pessoas_deve_retornar_200_quando_chamar_com_eduardo(client):
    response = client.get('/pessoa/eduardo')
    assert response.status_code == 200


def test_pessoas_deve_retornar_chamou_eduardo_quando_chamar_com_eduardo(client):
    response = client.get('/pessoa/eduardo')
    assert response.json() == {'message': 'Você chamou eduardo'}


# def test_busca_por_id_deve_retornar_404(client):
#     response = client.get('/id/42')
#     assert response.status_code == 404

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
        'id': 1,
        'nome': 'Regis',
        'idade': 42,
        'email': 'regis@email.com',
    }
    response = client.post('/inserir/', json=user)
    assert response.status_code == 201


def test_inserir_entidade_não_processável_retorna_422(client):
    user = {
        'nome': 'Regis',
        'email': 'regis@email.com',
    }
    response = client.post('/inserir/', json=user)
    assert response.status_code == 422


def test_pessoas_deve_retornar_200(client):
    response = client.get('/pessoas')
    assert response.status_code == 200


def test_pessoas_deve_retornar_lista_de_pessoas(client):
    response = client.get('/pessoas')
    pessoas = [
        {"id": 1, "nome": "Regis", "idade": 42, "email": "regis@email.com"}
    ]
    assert response.json() == pessoas


def test_get_pessoas_deve_retornar_200(client):
    response = client.get('/pessoas/1')
    assert response.status_code == 200


def test_get_pessoas_deve_retornar_um_dict(client):
    response = client.get('/pessoas/1')
    pessoa = {"id": 1, "nome": "Regis", "idade": 42, "email": "regis@email.com"}
    assert response.json() == pessoa


def test_pessoas_add_deve_retornar_201(client):
    pessoa = {"id": 1, "nome": "Regis", "idade": 42, "email": "regis@email.com"}
    response = client.post('/pessoas/add/', json=pessoa)
    assert response.status_code == 201
