"""add users and owner_id to todos

Revision ID: 20260316_0002
Revises: 20260316_0001
Create Date: 2026-03-16
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "20260316_0002"
down_revision = "20260316_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    tables = inspector.get_table_names()
    if "users" not in tables:
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("email", sa.String(), nullable=False),
            sa.Column("hashed_password", sa.String(), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )

    user_indexes = {idx["name"] for idx in inspector.get_indexes("users")}
    if "ix_users_email" not in user_indexes:
        op.create_index("ix_users_email", "users", ["email"], unique=True)

    todo_columns = {col["name"] for col in inspector.get_columns("todos")}
    if "owner_id" not in todo_columns:
        op.add_column("todos", sa.Column("owner_id", sa.Integer(), nullable=True))

    todo_indexes = {idx["name"] for idx in inspector.get_indexes("todos")}
    if "ix_todos_owner_id" not in todo_indexes:
        op.create_index("ix_todos_owner_id", "todos", ["owner_id"], unique=False)

    # SQLite cannot ALTER TABLE to add foreign key constraints directly.
    # We keep owner_id and enforce ownership in application logic.


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    todo_indexes = {idx["name"] for idx in inspector.get_indexes("todos")}
    if "ix_todos_owner_id" in todo_indexes:
        op.drop_index("ix_todos_owner_id", table_name="todos")

    todo_columns = {col["name"] for col in inspector.get_columns("todos")}
    if "owner_id" in todo_columns:
        op.drop_column("todos", "owner_id")

    if "users" in inspector.get_table_names():
        user_indexes = {idx["name"] for idx in inspector.get_indexes("users")}
        if "ix_users_email" in user_indexes:
            op.drop_index("ix_users_email", table_name="users")
        op.drop_table("users")
