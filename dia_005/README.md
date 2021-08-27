# Configuração inicial do banco
1 - alembic init -t async <diretorio> (sem -t async se for sync)
2 - configurar o metadata no env.py
    importar Base.metadata
    Atualizar os fields - compare_type=True
	Importar do env a url do banco
3 - Iniciar a primeira migração - `alembic revision --autogenerate`
4 - Aplicar a migração - alembic upgrade head

# Atualizar a base de dados
1 - Altera/cria nova tabela
2 - Garantir que estamos no head das migrações
3 - Criar nova revision - alembic revision --autogenerate
4 - Aplica a nova revisão - alembic upgrade head
