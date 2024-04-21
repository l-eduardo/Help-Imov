from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Imagens(Base):
    __tablename__ = 'IMOVEIS'

    id = Column(String(36), ForeignKey('IMAGENS.id'), primary_key=True, nullable=False, name='id')
    codigo = Column(Integer, nullable=False, name='codigo')
    endereco = Column(String(36), nullable=False, name='endereco')
