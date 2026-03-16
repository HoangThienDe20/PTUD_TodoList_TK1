"""create todos table

Revision ID: 20260316_0001
Revises: 
Create Date: 2026-03-16
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260316_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "todos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("is_done", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_todos_is_done", "todos", ["is_done"], unique=False)
    op.create_index("ix_todos_title", "todos", ["title"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_todos_title", table_name="todos")
    op.drop_index("ix_todos_is_done", table_name="todos")
    op.drop_table("todos")
