"""add last few columns to posts table

Revision ID: b15aed7a955e
Revises: 734d0a5e89d5
Create Date: 2022-01-04 02:07:58.872509

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import false


# revision identifiers, used by Alembic.
revision = 'b15aed7a955e'
down_revision = '734d0a5e89d5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts', 
        sa.Column('published',
                  sa.Boolean(), 
                  nullable=False,
                  server_default='TRUE'),
    )
    op.add_column(
        'posts',
        sa.Column('created_at',
                  sa.TIMESTAMP(timezone=True), 
                  nullable=False,
                  server_default=sa.text("NOW()")),
    )


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
