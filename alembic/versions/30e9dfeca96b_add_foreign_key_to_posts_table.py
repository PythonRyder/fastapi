"""add foreign key to posts table

Revision ID: 30e9dfeca96b
Revises: ffbb0c6ebd6b
Create Date: 2022-10-03 07:06:47.155052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30e9dfeca96b'
down_revision = 'ffbb0c6ebd6b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", source_table= "posts", referent_table= "users",
                            local_cols=["owner_id"], remote_cols=["user_id"], ondelete= "CASCADE" )
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
