from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel


class TodoTagLink(SQLModel, table=True):
    __tablename__ = "todo_tag_link"

    todo_id: Optional[int] = Field(default=None, foreign_key="todos.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tags.id", primary_key=True)


class TagModel(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    todos: list["TodoModel"] = Relationship(back_populates="tags", link_model=TodoTagLink)

if TYPE_CHECKING:
    from app.models.todo import TodoModel
