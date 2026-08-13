from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.document import DocumentExtractionResponse
from app.services.extractor import DocumentExtractorService
from app.services.ai import AIService

router = APIRouter()

@router.post("", response_model=DocumentExtractionResponse)
async def extract_document_content(
    file: UploadFile = File(..., alias="documento_upload")
):
    """
    Comentário: Endpoint assíncrono para extração e classificação de documentos via IA.
    """
    allowed_extensions = (".pdf", ".docx", ".xlsx", ".xls", ".csv", ".txt", ".png", ".jpg", ".jpeg")

    if not file.filename or not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(status_code=400, detail="Formato de arquivo não suportado.")

    extractor = DocumentExtractorService(file)
    ai_service = AIService() # <-- INSTANCIAR A IA

    try:
        # 1. OCR e Extração de Texto Bruto
        extracted_text = await extractor.process_document()
        
        # 2. Enviar para a IA classificar e estruturar
        structured_data = await ai_service.extract_and_classify(extracted_text)

        # RETORNO CORRIGIDO (Chaves em inglês, conteúdo em PT-BR)
        return DocumentExtractionResponse(
            status="success",
            message="Documento processado, classificado e estruturado pela IA com sucesso.",
            extracted_text=extracted_text,
            file_name=extractor.file_name,
            structured_data=structured_data 
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))