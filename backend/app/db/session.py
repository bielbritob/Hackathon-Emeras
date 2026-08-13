import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do .env
load_dotenv()

# Padrão Fallback da URL do Banco de Dados (usando o MySQL do Docker)
DEFAULT_DATABASE_URL = "mysql+pymysql://admin:adminpassword@localhost:3306/hackathon_db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

# Garante que o driver utilizado seja o pymysql (síncrono) para a SessionLocal
if DATABASE_URL and DATABASE_URL.startswith("mysql+aiomysql"):
    DATABASE_URL = DATABASE_URL.replace("mysql+aiomysql", "mysql+pymysql")

# Criação do motor do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica se a conexão com o MySQL está ativa antes de cada query
)

# Fábrica de sessões da base de dados (Exporta a classe SessionLocal)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)