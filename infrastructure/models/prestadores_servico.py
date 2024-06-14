from sqlalchemy import Column, Date, ForeignKey, Integer, String
from infrastructure.models import Base


#Base = declarative_base()

class PrestadoresServicos(Base):
    __tablename__ = 'PRESTADORES_SERVICOS'

    id = Column(String(36), ForeignKey('USUARIOS_IDENTITY_INFOS.id'), primary_key=True)
    nome = Column(String(255))
    data_nascimento = Column(Date, nullable=False, name='data_nascimento')
    especialidade = Column(String(255))
    empresa = Column(String(255))

    def __repr__(self):
        return f"PrestadorServicos(id={self.id}, nome='{self.nome}', especialidade='{self.especialidade}', empresa={self.empresa})"
