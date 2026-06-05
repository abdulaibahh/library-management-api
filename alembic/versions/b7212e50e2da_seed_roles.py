"""seed roles

Revision ID: b7212e50e2da
Revises: 7e46b0bad640
Create Date: 2026-06-05 19:16:13.073808
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "b7212e50e2da"
down_revision = '7e46b0bad640'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Idempotent insert for Postgres: skip if role already exists
    op.execute(
        """
        INSERT INTO roles (name) VALUES
        ('student'), ('librarian'), ('admin')
        ON CONFLICT (name) DO NOTHING;
        """
    )


def downgrade() -> None:
    op.execute("DELETE FROM roles WHERE name IN ('student', 'librarian', 'admin')")
