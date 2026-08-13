from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Comentário: Base partilhada (campos comuns na criação e leitura)
class EducationalActionBase(BaseModel):
    title: str
    requesting_unit: Optional[str] = None
    modality: Optional[str] = None

# Comentário: Schema usado quando o Frontend envia dados para CRIAR uma ação
class EducationalActionCreate(EducationalActionBase):
    pass # Por enquanto, criar só pede os campos base

# Comentário: Schema usado quando o Backend DEVOLVE os dados para o Frontend
class EducationalActionResponse(EducationalActionBase):
    id: int
    status: str
    attention_level: str
    completeness_percentage: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Truque Sénior: Isto permite que o Pydantic leia diretamente dos modelos do SQLAlchemy
    model_config = ConfigDict(from_attributes=True)