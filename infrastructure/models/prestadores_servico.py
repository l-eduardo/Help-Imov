from sqlalchemy import Column, ForeignKey, Integer, String
from infrastructure.models import Base


#Base = declarative_base()

class PrestadoresServicos(Base):
    __tablename__ = 'PRESTADORES_SERVICOS'

    id = Column(Integer, ForeignKey('USUARIOS_IDENTITY_INFOS.id'), primary_key=True)
    nome = Column(String(255))
    especialidade = Column(String(255))
    experiencia = Column(Integer)

    def __repr__(self):
        return f"PrestadorServicos(id={self.id}, nome='{self.nome}', especialidade='{self.especialidade}', experiencia={self.experiencia})"
