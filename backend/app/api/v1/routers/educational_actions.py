from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.schemas.educational_action import EducationalActionCreate, EducationalActionResponse
from app.repositories.educational_action import EducationalActionRepository
from app.repositories.document import DocumentRepository

router = APIRouter(prefix="/educational-actions", tags=["Ações Educacionais"])

@router.post("/", response_model=EducationalActionResponse, status_code=status.HTTP_201_CREATED)
def create_educational_action(
    action_in: EducationalActionCreate,
    db: Session = Depends(get_db)
):
    """
    Cria uma nova Ação Educacional na base de dados.
    """
    repository = EducationalActionRepository(db)
    new_action = repository.create(action_in)
    return new_action

@router.get("/", response_model=List[EducationalActionResponse])
def list_educational_actions(db: Session = Depends(get_db)):
    """
    Retorna a lista de todas as Ações Educacionais cadastradas.
    """
    repository = EducationalActionRepository(db)
    return repository.get_all()

@router.post("/from-document/{document_id}", response_model=EducationalActionResponse, status_code=status.HTTP_201_CREATED)
def create_action_from_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Cria uma nova Ação Educacional utilizando os dados (JSON) extraídos por um documento
    que está na Caixa de Entrada e vincula o documento a ela automaticamente.
    """
    doc_repo = DocumentRepository(db)
    action_repo = EducationalActionRepository(db)
    
    document = doc_repo.get_by_id(document_id)
    if not document or not document.structured_data:
        raise HTTPException(status_code=400, detail="Documento inválido ou sem dados estruturados da IA.")
    
    # Extrai os dados do JSON que o Gemini gerou
    ai_data = document.structured_data
    
    # Prepara o schema para criar a Ação
    action_in = EducationalActionCreate(
        title=ai_data.get("title", f"Nova Ação ({document.file_name})"),
        requesting_unit=ai_data.get("requesting_unit"),
        modality=ai_data.get("modality")
    )
    
    # 1. Cria a ação educacional no banco
    new_action = action_repo.create(action_in)
    
    # 2. Vincula o documento a esta nova ação
    doc_repo.link_to_educational_action(document.id, new_action.id)
    
    return new_action