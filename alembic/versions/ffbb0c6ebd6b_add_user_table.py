"""add user table

Revision ID: ffbb0c6ebd6b
Revises: cc33a266aa78
Create Date: 2022-10-03 06:52:26.787350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffbb0c6ebd6b'
down_revision = 'cc33a266aa78'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("user_id", sa.Integer(), nullable = False),
                    sa.Column("email", sa.String(), nullable = False),
                    sa.Column("password", sa.String(), nullable = False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                                server_default= sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint("user_id"),
                    sa.UniqueConstraint("email")
                    )


def downgrade() -> None:
    op.drop_table("users")
