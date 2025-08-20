from datetime import datetime

from sqlalchemy import DateTime, event
from sqlalchemy.orm import (
    Mapped,
    ORMExecuteState,
    Session,
    mapped_column,
    with_loader_criteria,
)

from src.app.models.core.registry import table_registry


@table_registry.mapped_as_dataclass()
class SoftDeleteMixin:
    __abstract__ = True

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, init=False, default=None
    )

    def delete(self):
        self.deleted_at = datetime.now()

    def restore(self):
        self.deleted_at = None

    @property
    def is_deleted(self):
        return self.deleted_at is not None


@event.listens_for(Session, 'do_orm_execute')
def _add_soft_delete_filter(execute_state: ORMExecuteState):
    if (
        execute_state.is_select
        and not execute_state.execution_options.get('skip_filter', False)
        and hasattr(execute_state.bind_mapper.class_, 'deleted_at')
    ):
        cls = execute_state.bind_mapper.class_
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                cls,
                lambda cls_: cls_.deleted_at.is_(None),
                include_aliases=True,
            )
        )
