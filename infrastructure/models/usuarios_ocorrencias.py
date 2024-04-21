from sqlalchemy import Column, ForeignKey, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UsuariosOcorrencias(Base):
    __tablename__ = 'IMAGENS'

    usuario_id = Column(String(36), ForeignKey('USUARIOS_IDENTITY_INFOS.id'), nullable=False, name='usuario_id')
    ocorrencia_id = Column(String(36), ForeignKey('OCORRENCIAS.id'), nullable=False, name='ocorrencia_id')

