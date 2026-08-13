# Comentário: Importa todas as models para que o Alembic ou o SQLAlchemy as encontrem
from app.models.base import Base
from app.models.user import User
from app.models.educational_action import EducationalAction
from app.models.document import Document
from app.models.audit_log import AuditLog