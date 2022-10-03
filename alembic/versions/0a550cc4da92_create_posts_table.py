"""create_posts_table

Revision ID: 0a550cc4da92
Revises: 4f146d9c497f
Create Date: 2022-10-03 00:05:14.384537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a550cc4da92'
down_revision = '4f146d9c497f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                        sa.Column("title", sa.String(), nullable=False))
    

#Handling all the rolling back new changes:
def downgrade() -> None:
    op.drop_table("posts")
    pass