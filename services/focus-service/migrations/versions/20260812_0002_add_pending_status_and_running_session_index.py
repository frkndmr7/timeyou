"""add pending status and running session index

Revision ID: 20260812_0002
Revises: 20260812_0001
Create Date: 2026-08-12

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "20260812_0002"
down_revision: Union[str, Sequence[str], None] = "20260812_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE session_status ADD VALUE IF NOT EXISTS 'pending'")
    op.create_index(
        "uq_focus_sessions_one_running_per_user",
        "focus_sessions",
        ["user_id"],
        unique=True,
        postgresql_where=sa.text("status = 'running'"),
    )


def downgrade() -> None:
    op.drop_index(
        "uq_focus_sessions_one_running_per_user",
        table_name="focus_sessions",
    )
    op.execute(
        "ALTER TABLE focus_sessions "
        "ALTER COLUMN status TYPE text"
    )
    op.execute("DROP TYPE session_status")
    op.execute(
        "CREATE TYPE session_status AS ENUM "
        "('running', 'completed', 'cancelled')"
    )
    op.execute(
        "ALTER TABLE focus_sessions "
        "ALTER COLUMN status TYPE session_status "
        "USING status::text::session_status"
    )
