"""set gender

Revision ID: 10ae6b3106d0
Revises: d65e9e2a2711
Create Date: 2023-10-08 17:35:35.387379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10ae6b3106d0'
down_revision: Union[str, None] = 'd65e9e2a2711'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('name', sa.String(), nullable=False))
    op.add_column('user', sa.Column('surname', sa.String(), nullable=False))
    op.add_column('user', sa.Column('patronymic', sa.String(), nullable=True))
    op.add_column('user', sa.Column('birth_date', sa.TIMESTAMP(), nullable=False))
    op.add_column('user', sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='genderenum'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'gender')
    op.drop_column('user', 'birth_date')
    op.drop_column('user', 'patronymic')
    op.drop_column('user', 'surname')
    op.drop_column('user', 'name')
    # ### end Alembic commands ###
