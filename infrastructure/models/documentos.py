from sqlalchemy import Column, ForeignKey, String, LargeBinary
from infrastructure.models import Base


#Base = declarative_base()

class Documentos(Base):
    __tablename__ = 'DOCUMENTOS'

    id = Column(String(36), primary_key=True, nullable=False, name='id')
    image = Column(LargeBinary, name='documentos')
    vistoria_id = Column(String(36), ForeignKey('VISTORIAS.id'), primary_key=True, name='id')

