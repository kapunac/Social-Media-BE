"""add user table

Revision ID: a37982e2b80f
Revises: 9fb08e42c8c8
Create Date: 2022-08-29 14:09:52.527308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a37982e2b80f'
down_revision = '9fb08e42c8c8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable= False),
    sa.Column('email', sa.String(), nullable= False),
    sa.Column('password', sa.String(), nullable= False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
