from sqlalchemy import Column, Date, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from infrastructure.models import Base

# Base = declarative_base()

class UsuariosIdentityInfos(Base):
    __tablename__ = 'USUARIOS_IDENTITY_INFOS'

    id = Column(String(36), primary_key=True)
    email = Column(String(255))
    senha = Column(String(255))

    def __repr__(self):
        return f'<UsuariosIdentityInfos(id={self.id}, email={self.email}, senha={self.senha})>'
