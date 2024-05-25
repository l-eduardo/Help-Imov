from sqlalchemy import Column, ForeignKey, String, LargeBinary
from infrastructure.models import Base


class UsuariosOcorrencias(Base):
    __tablename__ = 'USUARIOS_OCORRENCIAS'

    usuario_id = Column(String(36), ForeignKey('USUARIOS_IDENTITY_INFOS.id'), primary_key=True, nullable=False, name='usuario_id')
    ocorrencia_id = Column(String(36), ForeignKey('OCORRENCIAS.id'), primary_key=True, nullable=False, name='ocorrencia_id')

