from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.todo import TodoCreate, TodoListResponse, TodoOut, TodoPatch, TodoUpdate
from app.services.todo_service import service

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, session: Session = Depends(get_session)) -> TodoOut:
    return service.create(session, payload)


@router.get("", response_model=TodoListResponse)
def list_todos(
    session: Session = Depends(get_session),
    is_done: Optional[bool] = Query(None),
    q: Optional[str] = Query(None),
    sort: str = Query("-created_at"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> TodoListResponse:
    try:
        return service.list(session, is_done=is_done, q=q, sort=sort, limit=limit, offset=offset)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int, session: Session = Depends(get_session)) -> TodoOut:
    todo = service.get(session, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, payload: TodoUpdate, session: Session = Depends(get_session)) -> TodoOut:
    todo = service.update(session, todo_id, payload)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.patch("/{todo_id}", response_model=TodoOut)
def patch_todo(todo_id: int, payload: TodoPatch, session: Session = Depends(get_session)) -> TodoOut:
    todo = service.patch(session, todo_id, payload)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.post("/{todo_id}/complete", response_model=TodoOut)
def complete_todo(todo_id: int, session: Session = Depends(get_session)) -> TodoOut:
    todo = service.complete(session, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, session: Session = Depends(get_session)) -> None:
    ok = service.delete(session, todo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Todo not found")
    return None
