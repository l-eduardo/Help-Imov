from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Solicitacoes(Base):
    __tablename__ = 'SOLICITACOES'

    id = Column(String(36), primary_key=True, name='id')
    id_contrato = Column(String(36), ForeignKey('CONTRATOS.id') ,name='id_contrato')
    titulo = Column(String(36),name='titulo')
    descricao = Column(String(36),name='descricao')
    status = Column(String(36),name='status')
    prioridade = Column(String(36),name='prioridade')
    data_criacao = Column(String(36),name='data_criacao')