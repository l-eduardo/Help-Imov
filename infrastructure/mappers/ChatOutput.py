from typing import List

from sqlalchemy import UUID
from domain.models.chat import Chat
from domain.models.mensagem import Mensagem
from domain.models.ocorrencia import Ocorrencia
from infrastructure.mappers.ImagemOutput import ImagemOutputMapper
from infrastructure.models.chats import Chats
from infrastructure.models.imagens import Imagens
from infrastructure.models.mensagens import Mensagens
from datetime import datetime


class ChatOutputMapper:
    @staticmethod
    def map_chat(chat: Chat):
        chat_id = str(chat.id)
        chat_to_db = Chats(id = chat_id)
        return chat_to_db

    @staticmethod
    def map_mensagens(chat_id: UUID, mensagens: List[Mensagem]):
        lista_mensagens_to_db = [Mensagens(id=str(mensagem.id),
                                           chat_id=str(chat_id),
                                           usuario_id=str(mensagem.usuario.id),
                                           mensagem=mensagem.mensagem,
                                           datetime=mensagem.datetime) for mensagem in mensagens]
        return lista_mensagens_to_db

