"""add column to posts table

Revision ID: cbecbe676219
Revises: 769a94cc1a7f
Create Date: 2022-01-03 08:02:45.278646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbecbe676219'
down_revision = '769a94cc1a7f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
