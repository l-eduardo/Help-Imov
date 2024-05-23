from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from infrastructure.models import Base


#Base = declarative_base()

class Locatarios(Base):
    __tablename__ = 'LOCATARIOS'


    id = Column(Integer, ForeignKey('USUARIOS_IDENTITY_INFOS.id'),  primary_key=True)
    nome = Column(String(50), nullable=False, name='nome')
    data_nascimento = Column(Date, nullable=False, name='data_nascimento')

    #contrato = relationship()
