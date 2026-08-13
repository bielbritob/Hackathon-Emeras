from fastapi import APIRouter
from app.api.v1.routers import documents, educational_actions

# Comentário: Router central agregador de todas as rotas da V1
api_router = APIRouter()

# Comentário: Inclui os routers específicos de cada recurso
api_router.include_router(documents.router)

api_router.include_router(educational_actions.router)