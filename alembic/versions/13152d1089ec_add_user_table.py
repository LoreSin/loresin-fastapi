"""add user table

Revision ID: 13152d1089ec
Revises: cbecbe676219
Create Date: 2022-01-03 10:53:55.311676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13152d1089ec'
down_revision = 'cbecbe676219'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users', 
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade():
    op.drop_table('users')
