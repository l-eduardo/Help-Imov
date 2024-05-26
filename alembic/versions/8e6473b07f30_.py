"""empty message

Revision ID: 8e6473b07f30
Revises: a6d900222932
Create Date: 2024-05-25 21:17:15.965203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '8e6473b07f30'
down_revision: Union[str, None] = 'a6d900222932'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'IMAGENS', 'VISTORIAS', ['id_entidade'], ['id'])
    op.create_foreign_key(None, 'IMAGENS', 'OCORRENCIAS', ['id_entidade'], ['id'])
    op.add_column('VISTORIAS', sa.Column('descricao', sa.String(length=500), nullable=True))
    op.drop_constraint('VISTORIAS_ibfk_1', 'VISTORIAS', type_='foreignkey')
    op.drop_column('VISTORIAS', 'esta_fechada_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('VISTORIAS', sa.Column('esta_fechada_id', mysql.VARCHAR(length=36), nullable=True))
    op.create_foreign_key('VISTORIAS_ibfk_1', 'VISTORIAS', 'IMAGENS', ['id'], ['id'])
    op.drop_column('VISTORIAS', 'descricao')
    op.drop_constraint(None, 'IMAGENS', type_='foreignkey')
    op.drop_constraint(None, 'IMAGENS', type_='foreignkey')
    # ### end Alembic commands ###
