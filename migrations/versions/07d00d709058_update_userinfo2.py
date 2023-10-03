"""update userInfo2

Revision ID: 07d00d709058
Revises: d27f7aa7c5fe
Create Date: 2023-09-17 15:32:53.730991

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07d00d709058'
down_revision: Union[str, None] = 'd27f7aa7c5fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_info_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'user_info', ['user_info_id'], ['id'])
    op.add_column('user_info', sa.Column('avatar', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user_info', 'avatar', ['avatar'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_info', type_='foreignkey')
    op.drop_column('user_info', 'avatar')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'user_info_id')
    # ### end Alembic commands ###