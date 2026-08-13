from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class Document(Base):
    """
    Comentário: Tabela que armazena os PDFs/Imagens e o JSON extraído pela IA.
    Se educational_action_id for nulo, o documento fica na "Caixa de Entrada" aguardando vínculo.
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    
    # Chaves Estrangeiras
    educational_action_id = Column(Integer, ForeignKey("educational_actions.id"), nullable=True)
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False) # Rastreabilidade
    
    # Metadados do Arquivo
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False) # Onde o arquivo está salvo
    
    # Dados da Inteligência Artificial
    document_category = Column(String(100), nullable=True) # A string que o Gemini cuspiu
    extracted_text = Column(Text, nullable=True) # O texto bruto do OCR
    structured_data = Column(JSON, nullable=True) # O JSON perfeito que o Gemini gerou
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    educational_action = relationship("EducationalAction", back_populates="documents")
    uploader = relationship("User")