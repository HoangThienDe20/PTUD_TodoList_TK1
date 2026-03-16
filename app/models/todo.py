from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.tag import TodoTagLink


class TodoModel(SQLModel, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    title: str = Field(max_length=100, index=True)
    description: Optional[str] = Field(default=None)
    is_done: bool = Field(default=False, index=True)
    due_date: Optional[date] = Field(default=None, index=True)
    deleted_at: Optional[datetime] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    tags: list["TagModel"] = Relationship(back_populates="todos", link_model=TodoTagLink)


if TYPE_CHECKING:
    from app.models.tag import TagModel
