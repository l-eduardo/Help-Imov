from sqlalchemy import Column, ForeignKey, String, LargeBinary
from infrastructure.models import Base


class Imagens(Base):
    __tablename__ = 'IMAGENS'

    id = Column(String(36), primary_key=True, nullable=False, name='id')
    image = Column(LargeBinary, name='imagem')
