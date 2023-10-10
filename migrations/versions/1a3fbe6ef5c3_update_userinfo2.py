"""update userInfo2

Revision ID: 1a3fbe6ef5c3
Revises: 07d00d709058
Create Date: 2023-09-17 15:36:44.729692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a3fbe6ef5c3'
down_revision: Union[str, None] = '07d00d709058'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_info', sa.Column('avatar_id', sa.Integer(), nullable=True))
    op.drop_constraint('user_info_avatar_fkey', 'user_info', type_='foreignkey')
    op.create_foreign_key(None, 'user_info', 'avatar', ['avatar_id'], ['id'])
    op.drop_column('user_info', 'avatar')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_info', sa.Column('avatar', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user_info', type_='foreignkey')
    op.create_foreign_key('user_info_avatar_fkey', 'user_info', 'avatar', ['avatar'], ['id'])
    op.drop_column('user_info', 'avatar_id')
    # ### end Alembic commands ###
