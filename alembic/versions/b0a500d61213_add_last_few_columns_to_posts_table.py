"""add last few columns to posts table

Revision ID: b0a500d61213
Revises: be0ab70d8c81
Create Date: 2022-08-29 15:39:04.753538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0a500d61213'
down_revision = 'be0ab70d8c81'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable= False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone= True), nullable= False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
