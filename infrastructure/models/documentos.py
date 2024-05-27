from sqlalchemy import Column, ForeignKey, String, LargeBinary
from sqlalchemy.dialects.mysql import LONGBLOB
from infrastructure.models import Base


class Documentos(Base):
    __tablename__ = 'DOCUMENTOS'

    id = Column(String(36), primary_key=True, nullable=False, name='id')
    documento = Column(LargeBinary().with_variant(LONGBLOB, "mysql"), name='documento')
    tipo = Column(String(50), name='tipo', nullable=False)
