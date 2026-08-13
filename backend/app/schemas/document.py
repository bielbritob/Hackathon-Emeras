from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

# --- O QUE JÁ LÁ ESTAVA (Para a IA) ---
class DocumentExtractionResponse(BaseModel):
    status: str
    message: str
    extracted_text: str
    file_name: str
    structured_data: Optional[Dict[str, Any]] = None


# --- O QUE VAMOS ADICIONAR AGORA (Para a Base de Dados) ---
class DocumentBase(BaseModel):
    file_name: str
    file_path: str
    educational_action_id: Optional[int] = None # Fica nulo se for para a "Caixa de Entrada"

class DocumentCreate(DocumentBase):
    uploader_id: int
    document_category: Optional[str] = None
    extracted_text: Optional[str] = None
    structured_data: Optional[Dict[str, Any]] = None

class DocumentResponse(DocumentBase):
    id: int
    uploader_id: int
    document_category: Optional[str] = None
    structured_data: Optional[Dict[str, Any]] = None
    created_at: datetime

    # Permite leitura direta do SQLAlchemy
    model_config = ConfigDict(from_attributes=True)