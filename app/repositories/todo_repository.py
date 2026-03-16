from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.todo import TodoModel
from app.schemas.todo import TodoCreate, TodoPatch, TodoUpdate


class TodoRepository:
    def create(self, session: Session, payload: TodoCreate) -> TodoModel:
        now = datetime.utcnow()
        todo = TodoModel(
            title=payload.title,
            description=payload.description,
            is_done=False,
            created_at=now,
            updated_at=now,
        )
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    def list(
        self,
        session: Session,
        *,
        is_done: Optional[bool] = None,
        q: Optional[str] = None,
        sort: str = "-created_at",
        limit: int = 10,
        offset: int = 0,
    ) -> tuple[list[TodoModel], int]:
        stmt = select(TodoModel)
        count_stmt = select(func.count()).select_from(TodoModel)

        if is_done is not None:
            stmt = stmt.where(TodoModel.is_done == is_done)
            count_stmt = count_stmt.where(TodoModel.is_done == is_done)

        if q:
            keyword = f"%{q}%"
            stmt = stmt.where(TodoModel.title.ilike(keyword))
            count_stmt = count_stmt.where(TodoModel.title.ilike(keyword))

        if sort not in {"created_at", "-created_at"}:
            raise ValueError("invalid sort field")

        if sort.startswith("-"):
            stmt = stmt.order_by(TodoModel.created_at.desc())
        else:
            stmt = stmt.order_by(TodoModel.created_at.asc())

        items = session.exec(stmt.offset(offset).limit(limit)).all()
        total = session.exec(count_stmt).one()
        return items, int(total)

    def get(self, session: Session, todo_id: int) -> Optional[TodoModel]:
        return session.get(TodoModel, todo_id)

    def update(self, session: Session, todo_id: int, payload: TodoUpdate) -> Optional[TodoModel]:
        todo = session.get(TodoModel, todo_id)
        if not todo:
            return None
        todo.title = payload.title
        todo.description = payload.description
        todo.is_done = payload.is_done
        todo.updated_at = datetime.utcnow()
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    def patch(self, session: Session, todo_id: int, payload: TodoPatch) -> Optional[TodoModel]:
        todo = session.get(TodoModel, todo_id)
        if not todo:
            return None

        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(todo, key, value)
        todo.updated_at = datetime.utcnow()
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    def complete(self, session: Session, todo_id: int) -> Optional[TodoModel]:
        todo = session.get(TodoModel, todo_id)
        if not todo:
            return None
        todo.is_done = True
        todo.updated_at = datetime.utcnow()
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    def delete(self, session: Session, todo_id: int) -> bool:
        todo = session.get(TodoModel, todo_id)
        if not todo:
            return False
        session.delete(todo)
        session.commit()
        return True


repo = TodoRepository()
