from sqlalchemy import Column, ForeignKey, String, LargeBinary
from infrastructure.models import Base


class Imagens(Base):
    __tablename__ = 'IMAGENS'

    id = Column(String(36), primary_key=True, nullable=False, name='id')
    id_imovel = Column(String(36), ForeignKey("IMOVEIS.id"), primary_key=False, nullable=True, name='id_imovel')
    id_ocorrencia = Column(String(36), ForeignKey("OCORRENCIAS.id"), primary_key=False, nullable=True, name='id_ocorrencia')
    id_solicitacao = Column(String(36), ForeignKey("SOLICITACOES.id"), primary_key=False, nullable=True, name='id_solicitacao')
    id_vistoria = Column(String(36), ForeignKey("VISTORIAS.id"), primary_key=False, nullable=True, name='id_vistoria')
    image = Column(LargeBinary, name='imagem')
