"""add posts foreign key

Revision ID: be0ab70d8c81
Revises: a37982e2b80f
Create Date: 2022-08-29 14:29:34.486523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be0ab70d8c81'
down_revision = 'a37982e2b80f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable= False))
    op.create_foreign_key('post_users_fk', source_table= "posts", referent_table="users", local_cols=['user_id'],  remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'user_id')
    pass
