from sqlalchemy import Column, Date, ForeignKey, String
from infrastructure.models import Base


#Base = declarative_base()

class Ocorrencias(Base):
    __tablename__ = 'OCORRENCIAS'

    id = Column(String(36), primary_key=True, name='id')
    titulo = Column(String(36), name='titulo')
    descricao = Column(String(36), name='descricao')
    status = Column(String(36), name='status')
    prioridade = Column(String(36), name='prioridade')
    data_criacao = Column(String(36), name='data_criacao')
    id_contrato = Column(String(36), name='id_contrato')
