"""create post table

Revision ID: 769a94cc1a7f
Revises: 
Create Date: 2022-01-03 07:48:21.752258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '769a94cc1a7f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts", sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
