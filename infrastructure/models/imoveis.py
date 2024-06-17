from sqlalchemy import Column, ForeignKey, Integer, String
from infrastructure.models import Base
from sqlalchemy.orm import relationship


class Imoveis(Base):
    __tablename__ = 'IMOVEIS'

    id = Column(String(36), primary_key=True, name='id')
    codigo = Column(Integer, nullable=False, name='codigo')
    endereco = Column(String(36), nullable=False, name='endereco')
    imagens = relationship('Imagens', cascade='all, delete-orphan')
