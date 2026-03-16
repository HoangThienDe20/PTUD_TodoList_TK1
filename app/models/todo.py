from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TodoModel(SQLModel, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=100, index=True)
    description: Optional[str] = Field(default=None)
    is_done: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
