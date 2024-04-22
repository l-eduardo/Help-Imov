from sqlalchemy import Column, ForeignKey, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Imagens(Base):
    __tablename__ = 'IMAGENS'

    id = Column(String(36), primary_key=True, nullable=False, name='id')
    image = Column(LargeBinary, name='imagem')
