"""segunda_migração

Revision ID: c67c828932e8
Revises: 6a6f826fe5b8
Create Date: 2021-08-26 21:28:10.740296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c67c828932e8'
down_revision = '6a6f826fe5b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pessoa')
    op.alter_column('user', 'nome',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'nome',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.create_table('pessoa',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nome', sa.INTEGER(), nullable=True),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
