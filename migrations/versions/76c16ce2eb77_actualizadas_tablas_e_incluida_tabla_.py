"""Actualizadas tablas e incluida tabla Split

Revision ID: 76c16ce2eb77
Revises: bc569f22c047
Create Date: 2023-05-08 18:57:59.350614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76c16ce2eb77'
down_revision = 'bc569f22c047'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('role', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('position', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('matches', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('goals_conceded', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('penalties_saved', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('yellow_cards', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('red_cards', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('goals', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('assists', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('reflex', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('saves', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('kickoff', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('stretch', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('speed', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('physicality', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('shot', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('passing', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('talent', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('defense', sa.Integer(), nullable=True))
        batch_op.alter_column('mvp',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('player_name')
        batch_op.drop_column('posicion')
        batch_op.drop_column('goles')
        batch_op.drop_column('saque')
        batch_op.drop_column('t_amarilla')
        batch_op.drop_column('fisico')
        batch_op.drop_column('defensa')
        batch_op.drop_column('tiro')
        batch_op.drop_column('paradas')
        batch_op.drop_column('reflejo')
        batch_op.drop_column('goles_encajados')
        batch_op.drop_column('partidos')
        batch_op.drop_column('t_roja')
        batch_op.drop_column('pase')
        batch_op.drop_column('estirada')
        batch_op.drop_column('velocidad')
        batch_op.drop_column('asist')
        batch_op.drop_column('penaltis_parados')
        batch_op.drop_column('talento')

    with op.batch_alter_table('split', schema=None) as batch_op:
        batch_op.drop_constraint('split_name_key', type_='unique')
        batch_op.drop_column('end_date')
        batch_op.drop_column('name')

    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.add_column(sa.Column('points', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('position', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('victories', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('penalty_victories', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('penalty_defeats', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('defeats', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('goals_scored', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('goals_conceded', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('goals_difference', sa.Integer(), nullable=True))
        batch_op.drop_column('diferencia_goles')
        batch_op.drop_column('jugador_12_posicion')
        batch_op.drop_column('jugador_13_posicion')
        batch_op.drop_column('jugador_12_nombre')
        batch_op.drop_column('victorias')
        batch_op.drop_column('coach')
        batch_op.drop_column('jugador_11')
        batch_op.drop_column('victorias_penaltis')
        batch_op.drop_column('derrotas')
        batch_op.drop_column('goles_favor')
        batch_op.drop_column('goles_contra')
        batch_op.drop_column('derrotas_penaltis')
        batch_op.drop_column('jugador_13_nombre')
        batch_op.drop_column('entrenador')
        batch_op.drop_column('puntos')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.add_column(sa.Column('puntos', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('entrenador', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('jugador_13_nombre', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('derrotas_penaltis', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('goles_contra', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('goles_favor', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('derrotas', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('victorias_penaltis', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('jugador_11', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('coach', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('victorias', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('jugador_12_nombre', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('jugador_13_posicion', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('jugador_12_posicion', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('diferencia_goles', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_column('goals_difference')
        batch_op.drop_column('goals_conceded')
        batch_op.drop_column('goals_scored')
        batch_op.drop_column('defeats')
        batch_op.drop_column('penalty_defeats')
        batch_op.drop_column('penalty_victories')
        batch_op.drop_column('victories')
        batch_op.drop_column('position')
        batch_op.drop_column('points')

    with op.batch_alter_table('split', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('end_date', sa.DATE(), autoincrement=False, nullable=True))
        batch_op.create_unique_constraint('split_name_key', ['name'])

    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.add_column(sa.Column('talento', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('penaltis_parados', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('asist', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('velocidad', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('estirada', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('pase', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('t_roja', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('partidos', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('goles_encajados', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('reflejo', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('paradas', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('tiro', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('defensa', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('fisico', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('t_amarilla', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('saque', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('goles', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('posicion', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('player_name', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.alter_column('mvp',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('defense')
        batch_op.drop_column('talent')
        batch_op.drop_column('passing')
        batch_op.drop_column('shot')
        batch_op.drop_column('physicality')
        batch_op.drop_column('speed')
        batch_op.drop_column('stretch')
        batch_op.drop_column('kickoff')
        batch_op.drop_column('saves')
        batch_op.drop_column('reflex')
        batch_op.drop_column('assists')
        batch_op.drop_column('goals')
        batch_op.drop_column('red_cards')
        batch_op.drop_column('yellow_cards')
        batch_op.drop_column('penalties_saved')
        batch_op.drop_column('goals_conceded')
        batch_op.drop_column('matches')
        batch_op.drop_column('position')
        batch_op.drop_column('role')
        batch_op.drop_column('name')

    # ### end Alembic commands ###
