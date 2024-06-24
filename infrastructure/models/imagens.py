from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary
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

    id = Column(String(36), primary_key=True, name='id')
    id_imovel = Column(String(36), ForeignKey("IMOVEIS.id", ondelete="CASCADE",onupdate="CASCADE"), nullable=True, name='id_imovel')
    id_ocorrencia = Column(String(36), ForeignKey("OCORRENCIAS.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True, name='id_ocorrencia')
    id_vistoria = Column(String(36), ForeignKey("VISTORIAS.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True, name='id_vistoria')
    id_chat = Column(String(36), ForeignKey("CHATS.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True, name='id_chat')
    imagem = Column(LargeBinary().with_variant(LONGBLOB, "mysql"), name='imagem')
    tamanho = Column(Integer, nullable=False, name='tamanho')
    height = Column(Integer, nullable=False, name='height')
    width = Column(Integer, nullable=False, name='width')
    channels = Column(Integer, nullable=False, name='channels')

