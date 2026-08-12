from pydantic import BaseModel

class DocumentExtractionResponse(BaseModel):
    # Comentário: Modelo Pydantic para validação do retorno da API
    status: str
    message: str
    extracted_text: str
    file_name: str