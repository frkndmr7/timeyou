"""create focus_sessions table

Revision ID: 20260812_0001
Revises:
Create Date: 2026-08-12

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "20260812_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


session_status_enum = postgresql.ENUM(
    "running",
    "completed",
    "cancelled",
    name="session_status",
)


def upgrade() -> None:
    bind = op.get_bind()
    session_status_enum.create(bind, checkfirst=True)

    op.create_table(
        "focus_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("topic", sa.String(), nullable=False),
        sa.Column("planned_duration", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "status",
            postgresql.ENUM(
                "running",
                "completed",
                "cancelled",
                name="session_status",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "planned_duration >= 0",
            name="ck_focus_sessions_planned_duration_non_negative",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_focus_sessions_user_id",
        "focus_sessions",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_focus_sessions_user_id", table_name="focus_sessions")
    op.drop_table("focus_sessions")
    session_status_enum.drop(op.get_bind(), checkfirst=True)
