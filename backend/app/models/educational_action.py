from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class EducationalAction(Base):
    """
    Comentário: Tabela principal que representa um Curso/Evento.
    O "Motor de Atenção" usará os campos attention_level e completeness_percentage.
    """
    __tablename__ = "educational_actions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    requesting_unit = Column(String(150), nullable=True)
    modality = Column(String(50), nullable=True) # Ex: EAD, Presencial
    status = Column(String(50), default="DRAFT") # Ex: DRAFT, ACTIVE, COMPLETED
    
    # Indicadores Inteligentes (Calculados pela IA/Backend)
    attention_level = Column(String(20), default="REGULAR") # CRITICAL, WARNING, REGULAR
    completeness_percentage = Column(Float, default=0.0) # 0.0 a 100.0
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamento: Uma ação educacional tem muitos documentos
    documents = relationship("Document", back_populates="educational_action")