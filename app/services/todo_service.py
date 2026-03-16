from __future__ import annotations

from typing import Optional

from sqlmodel import Session

from app.models.user import UserModel
from app.repositories.todo_repository import repo
from app.schemas.todo import TodoCreate, TodoListResponse, TodoOut, TodoPatch, TodoUpdate


class TodoService:
    def __init__(self, repository=repo) -> None:
        self._repo = repository

    def create(self, session: Session, payload: TodoCreate, current_user: UserModel) -> TodoOut:
        return self._repo.create(session, payload, current_user.id)

    def list(
        self,
        session: Session,
        current_user: UserModel,
        *,
        is_done: Optional[bool] = None,
        q: Optional[str] = None,
        sort: str = "-created_at",
        limit: int = 10,
        offset: int = 0,
    ) -> TodoListResponse:
        items, total = self._repo.list(
            session,
            owner_id=current_user.id,
            is_done=is_done,
            q=q,
            sort=sort,
            limit=limit,
            offset=offset,
        )
        return TodoListResponse(items=items, total=total, limit=limit, offset=offset)

    def get(self, session: Session, todo_id: int, current_user: UserModel) -> Optional[TodoOut]:
        return self._repo.get(session, todo_id, current_user.id)

    def update(self, session: Session, todo_id: int, payload: TodoUpdate, current_user: UserModel) -> Optional[TodoOut]:
        return self._repo.update(session, todo_id, payload, current_user.id)

    def patch(self, session: Session, todo_id: int, payload: TodoPatch, current_user: UserModel) -> Optional[TodoOut]:
        return self._repo.patch(session, todo_id, payload, current_user.id)

    def complete(self, session: Session, todo_id: int, current_user: UserModel) -> Optional[TodoOut]:
        return self._repo.complete(session, todo_id, current_user.id)

    def delete(self, session: Session, todo_id: int, current_user: UserModel) -> bool:
        return self._repo.delete(session, todo_id, current_user.id)

    def overdue(self, session: Session, current_user: UserModel) -> list[TodoOut]:
        return self._repo.overdue(session, current_user.id)

    def today(self, session: Session, current_user: UserModel) -> list[TodoOut]:
        return self._repo.today(session, current_user.id)


service = TodoService()
