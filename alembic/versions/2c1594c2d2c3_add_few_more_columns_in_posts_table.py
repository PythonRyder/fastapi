"""add few more columns in posts table

Revision ID: 2c1594c2d2c3
Revises: 30e9dfeca96b
Create Date: 2022-10-03 07:24:35.336648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c1594c2d2c3'
down_revision = '30e9dfeca96b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False))

    pass


def downgrade() -> None:
    op.drop_column("posts","published")
    op.drop_column("posts", "created_at")
    pass
