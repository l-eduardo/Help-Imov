from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped
from infrastructure.models import Base
from infrastructure.models.chats import Chats
from infrastructure.models.usuarios_identity_infos import UsuariosIdentityInfos

class Mensagens(Base):
    __tablename__ = "MENSAGENS"

    id = Column(String(36), primary_key=True)
    chat_id = Column(String(36), ForeignKey("CHATS.id"), nullable=False, name='chat_id')
    usuario_id = Column(String(36), ForeignKey('USUARIOS_IDENTITY_INFOS.id'), name='usuario_id')
    datetime = Column(String(36), name='datetime')
    mensagem = Column(String(500), name='mensagem')

