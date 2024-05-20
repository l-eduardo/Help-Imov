
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from infrastructure.models import Base

#Base = declarative_base()

class Vistorias(Base):
    __tablename__ = 'VISTORIAS'

    id = Column(String(36), ForeignKey('IMAGENS.id'), primary_key=True, nullable=False, name='id')
    contra_vistoria = Column(String(36), ForeignKey('VISTORIAS.id'), name='contra_vistoria_id')
    e_contestacao = Column(String(36), name='e_contestacao_id')
    esta_fechada = Column(String(36), name='esta_fechada_id')
    imovel_id = Column(String(36), ForeignKey('IMOVEIS.id'), name='imovel_id')

    contrato = relationship()
