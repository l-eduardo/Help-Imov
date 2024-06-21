from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from infrastructure.models import Base
from infrastructure.models.ocorrencias import Ocorrencias
from infrastructure.models.usuarios_identity_infos import UsuariosIdentityInfos


class UsuariosOcorrencias(Base):
    __tablename__ = 'USUARIOS_OCORRENCIAS'

    ocorrencia_id = Column(String(36), ForeignKey('OCORRENCIAS.id'), primary_key=True, nullable=False, name='ocorrencia_id')
    ocorrencia = relationship('Ocorrencias', foreign_keys=[ocorrencia_id])
    usuario_id = Column(String(36), ForeignKey('USUARIOS_IDENTITY_INFOS.id'), nullable=False, name='usuario_id')
    usuario = relationship('UsuariosIdentityInfos', foreign_keys=[usuario_id])


