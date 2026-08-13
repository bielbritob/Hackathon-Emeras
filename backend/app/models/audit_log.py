from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base

class AuditLog(Base):
    """
    Comentário: Tabela de auditoria para rastreabilidade total (Exigência do Tribunal).
    Nenhum registro aqui é apagado.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False) # Ex: "DOCUMENT_UPLOADED", "ACTION_CREATED"
    target_table = Column(String(100), nullable=False) # Ex: "documents"
    target_id = Column(Integer, nullable=False) # O ID do documento ou da ação afetada
    details = Column(Text, nullable=True) # Informações extras
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())