from sqlalchemy import Column, Date, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, Mapped
from infrastructure.models import Base
from infrastructure.models.ocorrencias import Ocorrencias

class Chats(Base):
    __tablename__ = 'CHATS'

    id = Column(String(36), primary_key=True)
    ocorrencia_id = Column(String(36), ForeignKey('OCORRENCIAS.id'), name='ocorrencia_id')
    ocorrencia = relationship('Ocorrencias', uselist=False, cascade='all')
