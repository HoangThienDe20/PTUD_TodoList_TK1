from datetime import datetime

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = None


class TodoUpdate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    is_done: bool = False


class TodoPatch(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = None
    is_done: bool | None = None


class TodoOut(BaseModel):
    id: int
    title: str
    description: str | None
    is_done: bool
    created_at: datetime
    updated_at: datetime


class TodoListResponse(BaseModel):
    items: list[TodoOut]
    total: int
    limit: int
    offset: int
