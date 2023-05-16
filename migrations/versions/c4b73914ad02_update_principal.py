"""Update principal

Revision ID: c4b73914ad02
Revises: 916a76726bd9
Create Date: 2023-05-13 16:28:34.905132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4b73914ad02'
down_revision = '916a76726bd9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.alter_column('team_name',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)

    with op.batch_alter_table('split', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('split', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.alter_column('team_name',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###