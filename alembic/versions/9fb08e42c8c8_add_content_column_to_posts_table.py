"""add content column to posts table

Revision ID: 9fb08e42c8c8
Revises: 16e5479d9503
Create Date: 2022-08-29 13:47:54.361537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fb08e42c8c8'
down_revision = '16e5479d9503'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable= False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
