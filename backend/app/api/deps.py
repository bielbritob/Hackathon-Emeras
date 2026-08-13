from typing import Generator
from app.db.session import SessionLocal

def get_db() -> Generator:
    """
    Dependência global que fornece e fecha a sessão da base de dados para cada requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()