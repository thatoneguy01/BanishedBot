"""Adjust Account and add Trivia

Revision ID: d6be8b9fd22d
Revises: 643f0c3c7c14
Create Date: 2024-03-24 21:47:35.788506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import BanishedBot

# revision identifiers, used by Alembic.
revision: str = 'd6be8b9fd22d'
down_revision: Union[str, None] = '643f0c3c7c14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trivia',
    sa.Column('id', sa.Unicode(length=24), nullable=False),
    sa.Column('category', sa.Unicode(length=20), nullable=False),
    sa.Column('correct_answer', sa.UnicodeText(), nullable=False),
    sa.Column('all_answers', BanishedBot.database.models.trivia.Json(), nullable=False),
    sa.Column('question', sa.UnicodeText(), nullable=False),
    sa.Column('tags', BanishedBot.database.models.trivia.Json(), nullable=False),
    sa.Column('difficulty', sa.Unicode(length=6), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.drop_column('accounts', 'username')
    op.add_column('accounts', sa.Column('username', sa.Unicode(length=20), nullable=False, server_default=""))
    op.drop_column('accounts', 'balance')
    op.add_column('accounts', sa.Column('balance', sa.Integer(), nullable=False, server_default=str(0)))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('accounts', 'username')
    op.add_column('accounts', sa.Column('username', sa.Unicode(length=20), nullable=True))
    op.drop_column('accounts', 'balance')
    op.add_column('accounts', sa.Column('balance', sa.Integer(), nullable=True))
    op.drop_table('trivia')
    # ### end Alembic commands ###
