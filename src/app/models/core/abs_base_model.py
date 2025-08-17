from datetime import datetime

from sqlalchemy import Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from src.app.models.core.registry import table_registry


@table_registry.mapped_as_dataclass()
class AbsBaseModel:
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False, init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False, init=False
    )
