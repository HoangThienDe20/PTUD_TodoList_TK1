from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from app.db.session import get_session
from app.main import app

# Ensure models are imported so SQLModel.metadata includes all tables.
from app.models import tag, todo, user  # noqa: F401


@pytest.fixture()
def client() -> TestClient:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(engine)


def auth_headers(client: TestClient) -> dict[str, str]:
    email = f"user-{uuid4().hex[:8]}@example.com"
    password = "secret123"

    register_resp = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )
    assert register_resp.status_code == 201

    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert login_resp.status_code == 200

    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_todo_success(client: TestClient) -> None:
    headers = auth_headers(client)
    resp = client.post(
        "/api/v1/todos",
        json={"title": "Hoc pytest"},
        headers=headers,
    )

    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Hoc pytest"
    assert body["is_done"] is False


def test_create_todo_validation_fail(client: TestClient) -> None:
    headers = auth_headers(client)
    resp = client.post(
        "/api/v1/todos",
        json={"title": "a"},
        headers=headers,
    )

    assert resp.status_code == 422


def test_get_todo_not_found(client: TestClient) -> None:
    headers = auth_headers(client)
    resp = client.get("/api/v1/todos/99999", headers=headers)

    assert resp.status_code == 404


def test_create_todo_auth_fail(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/todos",
        json={"title": "Khong token"},
    )

    assert resp.status_code == 401


def test_soft_delete_hides_todo(client: TestClient) -> None:
    headers = auth_headers(client)

    created = client.post(
        "/api/v1/todos",
        json={"title": "Task se bi soft delete"},
        headers=headers,
    )
    assert created.status_code == 201
    todo_id = created.json()["id"]

    deleted = client.delete(f"/api/v1/todos/{todo_id}", headers=headers)
    assert deleted.status_code == 204

    get_after_delete = client.get(f"/api/v1/todos/{todo_id}", headers=headers)
    assert get_after_delete.status_code == 404

    listed = client.get("/api/v1/todos", headers=headers)
    assert listed.status_code == 200
    assert all(item["id"] != todo_id for item in listed.json()["items"])
