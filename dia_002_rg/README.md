# Dia 002

Após copiar a pasta rode

```
poetry install
poetry shell
```

Falamos sobre

- SQLAlchemy
- Pydantic
- Alembic

Para trabalhar com async vamos instalar

```
poetry add aiosqlite
poetry add sqlalchemy==1.4.18
```


O `run(create_database())` só funciona a partir do Python 3.8+


Rode o comando a seguir para criar o banco de dados.

```
python app/database.py
```

### Atividade

1. Fazer um método para buscar um usuário.
2. Fazer os 2 endpoints que estão faltando:
    * listar
    * deletar
3. Fazer o teste virar uma fixture.
4. Diminuir o código do método `pacth_user`.
