from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.document import Document
from app.schemas.document import DocumentCreate

class DocumentRepository:
    """
    Repositório responsável por executar operações de banco de dados na tabela documents.
    """
    def __init__(self, db_session: Session):
        self.__db_session = db_session

    def create(self, document_in: DocumentCreate) -> Document:
        """
        Persiste um novo documento no banco de dados.
        """
        new_document = Document(
            file_name=document_in.file_name,
            file_path=document_in.file_path,
            educational_action_id=document_in.educational_action_id,
            uploader_id=document_in.uploader_id,
            document_category=document_in.document_category,
            extracted_text=document_in.extracted_text,
            structured_data=document_in.structured_data
        )
        self.__db_session.add(new_document)
        self.__db_session.commit()
        self.__db_session.refresh(new_document)
        return new_document

    def get_by_id(self, document_id: int) -> Optional[Document]:
        """
        Busca um documento pelo ID.
        """
        return self.__db_session.query(Document).filter(Document.id == document_id).first()

    def get_unlinked_documents(self) -> List[Document]:
        """
        Retorna todos os documentos que estão na 'Caixa de Entrada' (sem Ação Educacional vinculada).
        """
        return self.__db_session.query(Document).filter(Document.educational_action_id.is_(None)).all()

    def link_to_educational_action(self, document_id: int, action_id: int) -> Optional[Document]:
        """
        Vincular um documento da Caixa de Entrada a uma Ação Educacional existente.
        """
        document = self.get_by_id(document_id)
        if document:
            document.educational_action_id = action_id
            self.__db_session.commit()
            self.__db_session.refresh(document)
        return document