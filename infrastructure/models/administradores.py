from sqlalchemy import Boolean, Column, Date, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Administradores(Base):
    __tablename__ = 'ADMINISTRADORES'

    id = Column(String(36), ForeignKey('USUARIOS_IDENTITY_INFOS.id'), primary_key=True)
    data_nascimento = Column(Date)
    nome = Column(String(255))
    e_root = Column(Boolean, name='is_root')

    def __repr__(self):
        return f'<Administrador(id={self.id}, data_nascimento={self.data_nascimento}, nome={self.nome}, e_root={self.e_root})>'
