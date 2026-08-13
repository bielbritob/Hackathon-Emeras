import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# 1. Tenta carregar as variáveis do .env (se existirem) baseado na raiz do backend
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "..", ".env")
load_dotenv(dotenv_path=env_path)

# 2. Importa a Base que contém todas as nossas tabelas registradas
from app.models import Base

# Objeto de configuração do Alembic
config = context.config

# Configuração de logs do Python
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Informa ao Alembic onde estão as nossas tabelas
target_metadata = Base.metadata

# 4. TRUQUE SÊNIOR: Padrão Fallback
# Se o DATABASE_URL não existir no .env, ele usa o banco do Docker local automaticamente!
DEFAULT_URL = "mysql+pymysql://admin:adminpassword@localhost:3306/hackathon_db"
db_url = os.getenv("DATABASE_URL", DEFAULT_URL)

# Garante que o Alembic sempre use o driver síncrono (pymysql)
if db_url and db_url.startswith("mysql+aiomysql"):
    db_url = db_url.replace("mysql+aiomysql", "mysql+pymysql")

config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()