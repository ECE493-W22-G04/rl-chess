"""Initial migration

Revision ID: b31e2ee53b90
Revises: 
Create Date: 2022-04-06 19:45:40.727803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b31e2ee53b90'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('games',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('black_player', sa.Integer(), nullable=True),
    sa.Column('white_player', sa.Integer(), nullable=True),
    sa.Column('winner', sa.Integer(), nullable=True),
    sa.Column('game_history', sa.Text(), nullable=True),
    sa.Column('is_pvp', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['black_player'], ['players.id'], ),
    sa.ForeignKeyConstraint(['white_player'], ['players.id'], ),
    sa.ForeignKeyConstraint(['winner'], ['players.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('games')
    op.drop_table('players')
    # ### end Alembic commands ###
