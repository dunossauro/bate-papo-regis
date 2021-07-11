# bate-papo-regis

Repositório destinado aos papos com o [Regis](https://github.com/rg3915). Sobre Python, é claro.


## Sobre as pastas

As pastas `dia_00*` foram feitas por mim (dunossauro).

As pastas `dia_00*rg` foram refeitas pelo Regis.

> Se você quiser, pode refazer também. =D


## Anotações

As anotações a seguir fazem parte dos assuntos discutidos nas conversas.

## Dia 01


poetry com Python 3.9

```
pyenv local 3.9.4
poetry install
```

```
poetry init -n
poetry add fastapi
```

Para rodar o FastAPI você precisa do uvicorn.

```
poetry add uvicorn
```

Instale o pytest.

```
poetry add --dev pytest
```

Entre no shell do poetry para o rodar o pytest.

```
poetry shell
```

```
pytest .
```

```
poetry add --dev requests
```

Para listar todas as fixtures

```
pytest --fixtures
```

#### Rodar a aplicação

```
uvicorn app:create_app
```

#### Testando BaseModel

```python
$ poetry shell


from pydantic import BaseModel

class User(BaseModel):
    nome: str
    idade: int
    email: str

User({'nome': 'Regis', 'idade': 42, 'email': 'regis@email.com'})
```

Se você deixar `idade: int = 42` no `UserSchema`, então vai quebrar o último teste.


### Resumo

* Criar recurso
* Passar path do parâmetro
* Fazer o cast do tipo
* Levantar exceção
* Fazer POST


### Atividade

Fazer um CRUD sem banco.

