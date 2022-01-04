"""add foreign-key to posts table

Revision ID: 734d0a5e89d5
Revises: 13152d1089ec
Create Date: 2022-01-03 10:55:56.474821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '734d0a5e89d5'
down_revision = '13152d1089ec'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk',
                          source_table='posts',
                          referent_table='users',
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete="CASCADE")


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
