from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.document import DocumentExtractionResponse
from app.services.extractor import DocumentExtractorService

router = APIRouter()

@router.post("", response_model=DocumentExtractionResponse)
async def extract_document_content(file: UploadFile = File(..., alias="documento_upload")):
    """
    Comentário: Endpoint assíncrono para extração de texto de documentos e imagens.
    """
    allowed_extensions = (".pdf", ".docx", ".xlsx", ".xls", ".csv", ".txt", ".png", ".jpg", ".jpeg")

    if not file.filename or not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Formato de arquivo não suportado. Envie documentos ou imagens (PDF, DOCX, XLSX, TXT, PNG, JPG)."
        )

    extractor = DocumentExtractorService(file)

    try:
        extracted_text = await extractor.process_document()

        return DocumentExtractionResponse(
            status="sucesso",
            message="Texto do documento extraído com sucesso.",
            extracted_text=extracted_text,
            file_name=extractor.file_name
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno durante a extração do documento: {str(e)}"
        )