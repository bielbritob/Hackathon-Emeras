from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.schemas.educational_action import EducationalActionCreate, EducationalActionResponse
from app.repositories.educational_action import EducationalActionRepository

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