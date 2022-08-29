"""create posts table

Revision ID: 16e5479d9503
Revises: 
Create Date: 2022-08-29 13:24:59.972592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16e5479d9503'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', 
    sa.Column('id', sa.Integer(), nullable= False, primary_key=True),
    sa.Column('title', sa.String(), nullable= False)
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
