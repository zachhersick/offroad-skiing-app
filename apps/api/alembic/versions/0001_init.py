"""initial schema

Revision ID: 0001_init
Revises:
Create Date: 2026-03-12
"""

from pathlib import Path

from alembic import op

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql = Path(__file__).resolve().parents[4] / "infra" / "migrations" / "001_init.sql"
    op.execute(sql.read_text())


def downgrade() -> None:
    for table in [
        "approvals",
        "artifacts",
        "step_logs",
        "agent_runs",
        "recommendations",
        "packing_lists",
        "conditions",
        "resort_entries",
        "trail_entries",
        "routes",
        "trips",
        "gear_items",
        "ski_quivers",
        "vehicles",
        "profiles",
        "users",
    ]:
        op.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
