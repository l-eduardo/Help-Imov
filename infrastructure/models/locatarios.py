from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped

from infrastructure.models import Base
from infrastructure.models.usuarios_identity_infos import UsuariosIdentityInfos


#Base = declarative_base()

class Locatarios(Base):
    __tablename__ = 'LOCATARIOS'


    id = Column(String(36), ForeignKey('USUARIOS_IDENTITY_INFOS.id'),  primary_key=True)
    nome = Column(String(50), nullable=False, name='nome')
    data_nascimento = Column(Date, nullable=False, name='data_nascimento')

    user_identity = relationship('UsuariosIdentityInfos')

    contratos = relationship('Contratos', back_populates='locatario', cascade='all, delete-orphan')

