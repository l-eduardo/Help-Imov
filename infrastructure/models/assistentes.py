from sqlalchemy import Column, Date, ForeignKey, Integer, String
from infrastructure.models import Base


#Base = declarative_base()

class Assistentes(Base):
    __tablename__ = 'ASSISTENTES'

    id = Column(String(36), ForeignKey('USUARIOS_IDENTITY_INFOS.id'), primary_key=True)
    nome = Column(String(50), name='nome')
    data_nascimento = Column(Date, name='data_nascimento')

