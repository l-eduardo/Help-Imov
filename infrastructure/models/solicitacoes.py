from sqlalchemy import Column, ForeignKey, String
from infrastructure.models import Base


class Solicitacoes(Base):
    __tablename__ = 'SOLICITACOES'

    id = Column(String(36), primary_key=True, name='id')
    titulo = Column(String(36),name='titulo')
    descricao = Column(String(36),name='descricao')
    status = Column(String(36),name='status')
#    prioridade = Column(String(36),name='prioridade')
    data_criacao = Column(String(36),name='data_criacao')
    id_contrato = Column(String(36), ForeignKey('CONTRATOS.id'), name='contrato_id')

