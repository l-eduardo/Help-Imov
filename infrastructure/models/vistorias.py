
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Vistorias(Base):
    __tablename__ = 'VISTORIAS'

    id = Column(String(36), ForeignKey('IMAGENS.id'), primary_key=True, nullable=False, name='id')
    contra_vistoria = Column(String(36), ForeignKey('VISTORIAS.id'), primary_key=True, name='id')
    e_contestacao = Column(String(36), primary_key=True, name='id')
    esta_fechada = Column(String(36), primary_key=True, name='id')
    imovel_id = Column(String(36), ForeignKey('IMOVEIS.id'), primary_key=True, name='id')

