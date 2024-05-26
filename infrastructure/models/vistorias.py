
from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, LargeBinary, String
from sqlalchemy.orm import relationship

from infrastructure.models import Base
if TYPE_CHECKING:
    from infrastructure.models.imagens import Imagens


class Vistorias(Base):
    __tablename__ = 'VISTORIAS'

    id = Column(String(36), primary_key=True, name='id')
    descricao = Column(String(500),name='descricao')
    #vistoria_id = Column(String(36), ForeignKey('VISTORIAS.id'), primary_key=True, name='vistoria_id')
    imagens = relationship('Imagens', cascade='all, delete-orphan')
