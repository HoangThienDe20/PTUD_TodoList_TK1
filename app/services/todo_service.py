from typing import Optional

from sqlmodel import Session

from app.repositories.todo_repository import repo
from app.schemas.todo import TodoCreate, TodoListResponse, TodoOut, TodoPatch, TodoUpdate


class TodoService:
    def __init__(self, repository=repo) -> None:
        self._repo = repository

    def create(self, session: Session, payload: TodoCreate) -> TodoOut:
        return self._repo.create(session, payload)

    def list(
        self,
        session: Session,
        *,
        is_done: Optional[bool] = None,
        q: Optional[str] = None,
        sort: str = "-created_at",
        limit: int = 10,
        offset: int = 0,
    ) -> TodoListResponse:
        items, total = self._repo.list(
            session,
            is_done=is_done,
            q=q,
            sort=sort,
            limit=limit,
            offset=offset,
        )
        return TodoListResponse(items=items, total=total, limit=limit, offset=offset)

    def get(self, session: Session, todo_id: int) -> Optional[TodoOut]:
        return self._repo.get(session, todo_id)

    def update(self, session: Session, todo_id: int, payload: TodoUpdate) -> Optional[TodoOut]:
        return self._repo.update(session, todo_id, payload)

    def patch(self, session: Session, todo_id: int, payload: TodoPatch) -> Optional[TodoOut]:
        return self._repo.patch(session, todo_id, payload)

    def complete(self, session: Session, todo_id: int) -> Optional[TodoOut]:
        return self._repo.complete(session, todo_id)

    def delete(self, session: Session, todo_id: int) -> bool:
        return self._repo.delete(session, todo_id)


service = TodoService()
