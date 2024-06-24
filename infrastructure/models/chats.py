from sqlalchemy import Column, Date, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, Mapped
from infrastructure.models import Base

class Chats(Base):
    __tablename__ = 'CHATS'

    id = Column(String(36), primary_key=True)
    mensagens = relationship('Mensagens', cascade='all, delete-orphan')
    imagens = relationship('Imagens', cascade='all, delete-orphan')

