"""empty message

Revision ID: ebadf9b80bef
Revises: 
Create Date: 2024-10-07 15:59:15.326866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry, Raster

# revision identifiers, used by Alembic.
revision: str = 'ebadf9b80bef'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Criação da tabela 'users'
    op.create_table('users',
        sa.Column('id_users', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('password', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id_users'),
        schema='system_users'
    )
    
    # Criação da tabela 'farms'
    op.create_table('farms',
        sa.Column('id_farm', sa.Integer(), nullable=False),
        sa.Column('farm_code', sa.String(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['system_users.users.id_users'], ),
        sa.PrimaryKeyConstraint('id_farm'),
        schema='system_users'
    )
    
    # Criação da tabela 'fields'
    op.create_table('fields',
        sa.Column('id_field', sa.Integer(), nullable=False),
        sa.Column('field_code', sa.String(), nullable=True),
        sa.Column('poligono', Geometry(geometry_type='POLYGON', from_text='ST_GeomFromEWKT'), nullable=True),
        sa.Column('hectare', sa.Float(), nullable=True),
        sa.Column('farm_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['farm_id'], ['system_users.farms.id_farm'], ),
        sa.PrimaryKeyConstraint('id_field'),
        schema='system_users'
    )
    
    # Criação da tabela 'pins'
    op.create_table('pins',
        sa.Column('id_pins', sa.Integer(), nullable=False),
        sa.Column('point', Geometry(geometry_type='POINT', from_text='ST_GeomFromEWKT'), nullable=True),
        sa.Column('diagnostic', sa.Integer(), nullable=True),
        sa.Column('value', sa.Integer(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
        sa.Column('id_field', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['id_field'], ['system_users.fields.id_field'], ),
        sa.PrimaryKeyConstraint('id_pins'),
        schema='system_users'
    )
    
    # Criação da tabela 'interpolation'
    op.create_table('interpolation',
        sa.Column('id_interpol', sa.Integer(), nullable=False),
        sa.Column('raster', Raster(from_text='raster'), nullable=True),  # Aqui está o Raster
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('field_id', sa.Integer(), nullable=True),
        sa.Column('pins_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['field_id'], ['system_users.fields.id_field'], ),
        sa.ForeignKeyConstraint(['pins_id'], ['system_users.pins.id_pins'], ),
        sa.PrimaryKeyConstraint('id_interpol'),
        schema='system_users'
    )

def downgrade() -> None:
    op.drop_table('interpolation', schema='system_users')
    op.drop_table('pins', schema='system_users')
    op.drop_table('fields', schema='system_users')
    op.drop_table('farms', schema='system_users')
    op.drop_table('users', schema='system_users')
