"""create posts table

Revision ID: 4f146d9c497f
Revises: 
Create Date: 2022-10-02 23:44:57.641401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f146d9c497f'
down_revision = None
branch_labels = None
depends_on = None

#Handling all the new changes:
def upgrade() -> None:
    op.create_table("posts", sa.Column('post_id', sa.Integer(), nullable=False, primary_key=True),
                        sa.Column("title", sa.String(), nullable=False))
    

#Handling all the rolling back new changes:
def downgrade() -> None:
    op.drop_table("posts")
    pass
