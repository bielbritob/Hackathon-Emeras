from fastapi import APIRouter
from app.api.v1.routers import documents

# Comentário: Router central agregador de todas as rotas da V1
api_router = APIRouter()

# Comentário: Define o prefixo da rota para /documentos e centraliza a tag da documentação
api_router.include_router(documents.router, prefix="/documentos", tags=["Documentos"])