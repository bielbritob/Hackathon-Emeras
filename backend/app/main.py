from fastapi import FastAPI
from app.api.v1.api import api_router

# Inicializa o aplicativo FastAPI 
app = FastAPI(
    title="EMERON Gestão Inteligente API",
    description="Backend estruturado com FastAPI, SQLAlchemy e MySQL",
    version="0.1.0",
)

# Comentário: Registro do roteador da V1 com o prefixo global /api/v1
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Status"])
async def health_check():
    """
    Comentário: Rota de verificação do estado operacional da API.
    """
    return {"status": "operacional", "mensagem": "API do EMERON Gestão Inteligente rodando com sucesso."}