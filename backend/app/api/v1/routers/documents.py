import os
import uuid
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.deps import get_db
from app.schemas.document import DocumentResponse, DocumentCreate
from app.repositories.document import DocumentRepository
from app.services.extractor import DocumentExtractorService
from app.services.ai import AIService

router = APIRouter(prefix="/documents", tags=["Central de Documentos"])

# Pasta para salvar os arquivos físicos
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_and_process_document(
    file: UploadFile = File(...),
    educational_action_id: Optional[int] = Form(None),
    uploader_id: int = Form(1), 
    db: Session = Depends(get_db)
):
    """
    Recebe um documento, executa OCR/extração de texto, 
    processa a inteligência estruturada com Gemini e salva na base de dados.
    """
    allowed_extensions = (".pdf", ".docx", ".xlsx", ".xls", ".csv", ".txt", ".png", ".jpg", ".jpeg")
    
    if not file.filename or not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(status_code=400, detail="Formato de arquivo não suportado.")

    # 1. OCR e Extração de Texto Bruto (USANDO O SEU CÓDIGO ORIGINAL QUE FUNCIONAVA)
    extractor = DocumentExtractorService(file)
    try:
        extracted_text = await extractor.process_document()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na extração de texto: {str(e)}")

    # 2. Processa a estruturação dos dados via Gemini AI
    ai_service = AIService()
    try:
        ai_result = await ai_service.extract_and_classify(extracted_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na inteligência artificial: {str(e)}")

    # 3. Agora que extraiu, salva o arquivo físico no disco para histórico
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Volta o ponteiro do arquivo para o início, pois o extractor já leu os bytes
    await file.seek(0)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 4. Prepara os dados para salvar no MySQL
    document_in = DocumentCreate(
        file_name=file.filename,
        file_path=file_path,
        educational_action_id=educational_action_id,
        uploader_id=uploader_id,
        document_category=ai_result.get("category", "Desconhecido"),
        extracted_text=extracted_text,
        structured_data=ai_result
    )

    # 5. Persiste no banco usando o Repositório
    repository = DocumentRepository(db)
    saved_document = repository.create(document_in)

    return saved_document