
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from infrastructure.models import Base


class Vistorias(Base):
    __tablename__ = 'VISTORIAS'

    id = Column(String(36), ForeignKey('IMAGENS.id'), primary_key=True, name='id')
    esta_fechada = Column(String(36), name='esta_fechada_id')
