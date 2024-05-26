from sqlalchemy import Column, Date, Enum, ForeignKey, String
from domain.enums.status import Status
from infrastructure.models import Base

from sqlalchemy.orm import relationship


class Solicitacoes(Base):
    __tablename__ = 'SOLICITACOES'

    id = Column(String(36), primary_key=True, name='id')
    titulo = Column(String(36),name='titulo')
    descricao = Column(String(36),name='descricao')
    status = Column(Enum(Status), name='status')
#    prioridade = Column(String(36),name='prioridade')
    data_criacao = Column(String(36),name='data_criacao')
    id_contrato = Column(String(36), ForeignKey('CONTRATOS.id'), name='contrato_id')

    imagens = relationship('Imagens', cascade='all, delete-orphan')