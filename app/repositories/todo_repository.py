from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.models.tag import TagModel
from app.models.todo import TodoModel
from app.schemas.todo import TodoOut
from app.schemas.todo import TodoCreate, TodoPatch, TodoUpdate


class TodoRepository:
    @staticmethod
    def _normalize_tags(tags: list[str]) -> list[str]:
        cleaned = [tag.strip().lower() for tag in tags if tag and tag.strip()]
        # Preserve order while deduplicating
        return list(dict.fromkeys(cleaned))

    def _get_or_create_tags(self, session: Session, tag_names: list[str]) -> list[TagModel]:
        normalized = self._normalize_tags(tag_names)
        if not normalized:
            return []

        stmt = select(TagModel).where(TagModel.name.in_(normalized))
        existing = session.exec(stmt).all()
        existing_map = {tag.name: tag for tag in existing}

        result: list[TagModel] = []
        for name in normalized:
            tag = existing_map.get(name)
            if tag is None:
                tag = TagModel(name=name)
                session.add(tag)
                session.flush()
                existing_map[name] = tag
            result.append(tag)
        return result

    @staticmethod
    def _to_out(todo: TodoModel) -> TodoOut:
        return TodoOut(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            due_date=todo.due_date,
            tags=[t.name for t in todo.tags],
            is_done=todo.is_done,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )

    def create(self, session: Session, payload: TodoCreate, owner_id: int) -> TodoOut:
        now = datetime.utcnow()
        todo = TodoModel(
            owner_id=owner_id,
            title=payload.title,
            description=payload.description,
            is_done=False,
            due_date=payload.due_date,
            created_at=now,
            updated_at=now,
        )
        todo.tags = self._get_or_create_tags(session, payload.tags)
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return self._to_out(todo)

    def list(
        self,
        session: Session,
        *,
        owner_id: int,
        is_done: Optional[bool] = None,
        q: Optional[str] = None,
        sort: str = "-created_at",
        limit: int = 10,
        offset: int = 0,
    ) -> tuple[list[TodoOut], int]:
        stmt = select(TodoModel).options(selectinload(TodoModel.tags))
        count_stmt = select(func.count()).select_from(TodoModel)

        stmt = stmt.where(TodoModel.owner_id == owner_id)
        count_stmt = count_stmt.where(TodoModel.owner_id == owner_id)

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
        return [self._to_out(item) for item in items], int(total)

    def get(self, session: Session, todo_id: int, owner_id: int) -> Optional[TodoOut]:
        stmt = (
            select(TodoModel)
            .options(selectinload(TodoModel.tags))
            .where(TodoModel.id == todo_id, TodoModel.owner_id == owner_id)
        )
        todo = session.exec(stmt).first()
        if not todo:
            return None
        return self._to_out(todo)

    def update(self, session: Session, todo_id: int, payload: TodoUpdate, owner_id: int) -> Optional[TodoOut]:
        todo = session.get(TodoModel, todo_id)
        if not todo:
            return None
        if todo.owner_id != owner_id:
            return None
        todo.title = payload.title
        todo.description = payload.description
        todo.due_date = payload.due_date
        todo.tags = self._get_or_create_tags(session, payload.tags)
        todo.is_done = payload.is_done
        todo.updated_at = datetime.utcnow()
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return self._to_out(todo)

    def patch(self, session: Session, todo_id: int, payload: TodoPatch, owner_id: int) -> Optional[TodoOut]:
        todo = session.get(TodoModel, todo_id)
        if not todo:
            return None
        if todo.owner_id != owner_id:
            return None

        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            if key == "tags" and value is not None:
                todo.tags = self._get_or_create_tags(session, value)
            else:
                setattr(todo, key, value)
        todo.updated_at = datetime.utcnow()
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return self._to_out(todo)

    def complete(self, session: Session, todo_id: int, owner_id: int) -> Optional[TodoOut]:
        todo = session.get(TodoModel, todo_id)
        if not todo:
            return None
        if todo.owner_id != owner_id:
            return None
        todo.is_done = True
        todo.updated_at = datetime.utcnow()
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return self._to_out(todo)

    def delete(self, session: Session, todo_id: int, owner_id: int) -> bool:
        todo = session.get(TodoModel, todo_id)
        if not todo:
            return False
        if todo.owner_id != owner_id:
            return False
        session.delete(todo)
        session.commit()
        return True

    def overdue(self, session: Session, owner_id: int) -> list[TodoOut]:
        today = date.today()
        stmt = (
            select(TodoModel)
            .options(selectinload(TodoModel.tags))
            .where(
                TodoModel.owner_id == owner_id,
                TodoModel.is_done == False,
                TodoModel.due_date.is_not(None),
                TodoModel.due_date < today,
            )
            .order_by(TodoModel.due_date.asc())
        )
        items = session.exec(stmt).all()
        return [self._to_out(item) for item in items]

    def today(self, session: Session, owner_id: int) -> list[TodoOut]:
        today = date.today()
        stmt = (
            select(TodoModel)
            .options(selectinload(TodoModel.tags))
            .where(
                TodoModel.owner_id == owner_id,
                TodoModel.is_done == False,
                TodoModel.due_date == today,
            )
            .order_by(TodoModel.created_at.asc())
        )
        items = session.exec(stmt).all()
        return [self._to_out(item) for item in items]


repo = TodoRepository()
