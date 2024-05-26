from sqlalchemy import Column, ForeignKey, String, LargeBinary
from sqlalchemy.dialects.mysql import LONGBLOB
from typing import TYPE_CHECKING

# if TYPE_CHECKING:
from infrastructure.models.imoveis import Imoveis
from infrastructure.models.ocorrencias import Ocorrencias
from infrastructure.models.solicitacoes import Solicitacoes
from infrastructure.models.vistorias import Vistorias
from infrastructure.models import Base



class Imagens(Base):
    __tablename__ = 'IMAGENS'

    id = Column(String(36), primary_key=True, nullable=False, name='id')
    id_imovel = Column(String(36), ForeignKey("IMOVEIS.id"), primary_key=False, nullable=True, name='id_imovel')
    id_ocorrencia = Column(String(36), ForeignKey("OCORRENCIAS.id"), primary_key=False, nullable=True, name='id_ocorrencia')
    id_solicitacao = Column(String(36), ForeignKey("SOLICITACOES.id"), primary_key=False, nullable=True, name='id_solicitacao')
    id_vistoria = Column(String(36), ForeignKey("VISTORIAS.id"), primary_key=False, nullable=True, name='id_vistoria')
    image = Column(LargeBinary().with_variant(LONGBLOB, "mysql"), name='imagem')
