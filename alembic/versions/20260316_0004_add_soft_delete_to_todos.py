"""add soft delete to todos

Revision ID: 20260316_0004
Revises: 20260316_0003
Create Date: 2026-03-16
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "20260316_0004"
down_revision = "20260316_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    todo_cols = {c["name"] for c in inspector.get_columns("todos")}
    if "deleted_at" not in todo_cols:
        op.add_column("todos", sa.Column("deleted_at", sa.DateTime(), nullable=True))

    todo_indexes = {idx["name"] for idx in inspector.get_indexes("todos")}
    if "ix_todos_deleted_at" not in todo_indexes:
        op.create_index("ix_todos_deleted_at", "todos", ["deleted_at"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    todo_indexes = {idx["name"] for idx in inspector.get_indexes("todos")}
    if "ix_todos_deleted_at" in todo_indexes:
        op.drop_index("ix_todos_deleted_at", table_name="todos")

    todo_cols = {c["name"] for c in inspector.get_columns("todos")}
    if "deleted_at" in todo_cols:
        op.drop_column("todos", "deleted_at")
