from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Assistentes(Base):
    __tablename__ = 'ASSISTENTES'

    id = Column(Integer, ForeignKey('USUARIOS_IDENTITY_INFOS.id'), primary_key=True)
    nome = Column(String(50), name='nome')
    data_nascimento = Column(Date, name='data_nascimento')

    def __repr__(self):
        return f"<Assistente(id={self.id}, nome='{self.nome}', email='{self.email}')>"
