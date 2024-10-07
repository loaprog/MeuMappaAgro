from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from backend.src.models.users import Users
from backend.src.models.farms import Farms
from backend.src.models.fields import Fields
from backend.src.models.pins import Pins
from backend.src.models.interpolation import Interpolation
from backend.src.models import Base

# Este é o objeto de configuração do Alembic, que fornece
# acesso aos valores no arquivo .ini em uso.
config = context.config

# Interpreta o arquivo de configuração para o log do Python.
# Esta linha configura basicamente os loggers.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Adicione o objeto MetaData do seu modelo aqui
# para suporte ao 'autogenerate'
target_metadata = Base.metadata  # Define a metadata para seus modelos

# Função para ignorar a tabela 'spatial_ref_sys'
def include_object(object, name, type_, reflected, compare_to):
    # Ignora a tabela 'spatial_ref_sys'
    if name == 'spatial_ref_sys':
        return False
    return True

def run_migrations_offline() -> None:
    """Executa as migrações no modo 'offline'.
    Isso configura o contexto apenas com uma URL
    e não com um Engine, embora um Engine também seja aceitável
    aqui. Ao pular a criação do Engine
    não precisamos nem de um DBAPI disponível.
    As chamadas para context.execute() aqui emitem a string fornecida na
    saída do script.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object  # Adiciona o filtro aqui para o modo offline
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa as migrações no modo 'online'.
    Nesse cenário, precisamos criar um Engine
    e associar uma conexão ao contexto.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object  # Adiciona o filtro aqui para o modo online
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
