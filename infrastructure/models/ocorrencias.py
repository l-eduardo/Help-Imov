from typing import TYPE_CHECKING
from sqlalchemy import Column, Date, Enum, ForeignKey, String
from domain.enums.status import Status
from infrastructure.models import Base
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from infrastructure.models.imagens import Imagens


class Ocorrencias(Base):
    __tablename__ = 'OCORRENCIAS'

    id = Column(String(36), primary_key=True, name='id')
    titulo = Column(String(25), name='titulo')
    descricao = Column(String(500), name='descricao')
    status = Column(Enum(Status), name='status')
    data_criacao = Column(Date, name='data_criacao')
    contrato_id = Column(String(36), ForeignKey('CONTRATOS.id'), name='id_contrato')
    criador_id = Column(String(36), ForeignKey('USUARIOS_IDENTITY_INFOS.id'), name='criador_id')

    imagens = relationship('Imagens', cascade='all, delete-orphan')
