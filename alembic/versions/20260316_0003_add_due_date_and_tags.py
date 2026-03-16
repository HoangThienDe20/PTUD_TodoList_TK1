"""add due_date and tags

Revision ID: 20260316_0003
Revises: 20260316_0002
Create Date: 2026-03-16
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "20260316_0003"
down_revision = "20260316_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    todo_cols = {c["name"] for c in inspector.get_columns("todos")}
    if "due_date" not in todo_cols:
        op.add_column("todos", sa.Column("due_date", sa.Date(), nullable=True))

    todo_indexes = {idx["name"] for idx in inspector.get_indexes("todos")}
    if "ix_todos_due_date" not in todo_indexes:
        op.create_index("ix_todos_due_date", "todos", ["due_date"], unique=False)

    tables = inspector.get_table_names()
    if "tags" not in tables:
        op.create_table(
            "tags",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )

    tag_indexes = {idx["name"] for idx in inspector.get_indexes("tags")}
    if "ix_tags_name" not in tag_indexes:
        op.create_index("ix_tags_name", "tags", ["name"], unique=True)

    if "todo_tag_link" not in tables:
        op.create_table(
            "todo_tag_link",
            sa.Column("todo_id", sa.Integer(), nullable=False),
            sa.Column("tag_id", sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(["todo_id"], ["todos.id"]),
            sa.ForeignKeyConstraint(["tag_id"], ["tags.id"]),
            sa.PrimaryKeyConstraint("todo_id", "tag_id"),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    tables = inspector.get_table_names()
    if "todo_tag_link" in tables:
        op.drop_table("todo_tag_link")

    if "tags" in tables:
        tag_indexes = {idx["name"] for idx in inspector.get_indexes("tags")}
        if "ix_tags_name" in tag_indexes:
            op.drop_index("ix_tags_name", table_name="tags")
        op.drop_table("tags")

    todo_indexes = {idx["name"] for idx in inspector.get_indexes("todos")}
    if "ix_todos_due_date" in todo_indexes:
        op.drop_index("ix_todos_due_date", table_name="todos")

    todo_cols = {c["name"] for c in inspector.get_columns("todos")}
    if "due_date" in todo_cols:
        op.drop_column("todos", "due_date")
