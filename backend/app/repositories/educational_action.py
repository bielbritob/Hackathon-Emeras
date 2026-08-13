from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.educational_action import EducationalAction
from app.schemas.educational_action import EducationalActionCreate

class EducationalActionRepository:
    """
    Repositório responsável por executar operações na tabela educational_actions.
    """
    def __init__(self, db_session: Session):
        self.__db_session = db_session

    def create(self, action_data: EducationalActionCreate) -> EducationalAction:
        new_action = EducationalAction(
            title=action_data.title,
            requesting_unit=action_data.requesting_unit,
            modality=action_data.modality
        )
        self.__db_session.add(new_action)
        self.__db_session.commit()
        self.__db_session.refresh(new_action)
        return new_action

    def get_all(self) -> List[EducationalAction]:
        return self.__db_session.query(EducationalAction).all()

    def get_by_id(self, action_id: int) -> Optional[EducationalAction]:
        return self.__db_session.query(EducationalAction).filter(EducationalAction.id == action_id).first()