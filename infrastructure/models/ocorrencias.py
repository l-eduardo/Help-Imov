from sqlalchemy import Column, Date, ForeignKey, String
from infrastructure.models import Base
from sqlalchemy.orm import relationship, Mapped



class Ocorrencias(Base):
    __tablename__ = 'OCORRENCIAS'

    id = Column(String(36), primary_key=True, name='id')
    titulo = Column(String(36), name='titulo')
    descricao = Column(String(36), name='descricao')
    status = Column(String(36), name='status')
    data_criacao = Column(String(36), name='data_criacao')

    contrato_id = Column(String(36), ForeignKey('CONTRATOS.id'), name='id_contrato')
