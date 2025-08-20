from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_declarative_extensions.audit import audit

from src.app.models.core.model_mixin import ModelMixin
from src.app.models.core.registry import table_registry
from src.app.models.core.soft_delete_mixin import SoftDeleteMixin


@audit(ignore_columns={'password', 'created_by', 'created_at'})
@table_registry.mapped_as_dataclass()
class UserModel(ModelMixin, SoftDeleteMixin):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
