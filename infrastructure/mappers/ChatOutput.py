from typing import List

from sqlalchemy import UUID
from domain.models.chat import Chat
from domain.models.ocorrencia import Ocorrencia
from infrastructure.models.chats import Chats
from infrastructure.models.mensagens import Mensagens
from datetime import datetime


class ChatOutputMapper:
    @staticmethod
    def map_chat(chat: Chat, ocorrencia: Ocorrencia):
        chat_id = str(chat.id)
        ocorrencia_id = str(ocorrencia.id)
        chat_to_db = Chats(id = chat_id, ocorrencia = ocorrencia_id)
        return chat_to_db
    
    @staticmethod
    def map_mensagens(chat_id: UUID, mensagens: List[tuple]):
        #mensagens: List[tuple[uuid.UUID, Usuario, str, date]],
        lista_mensagens_to_db = [Mensagens(id=str(mensagem[0]),
                                           chat=str(chat_id),
                                           usuario=str(mensagem[1]),
                                           mensagem=mensagem[2],
                                           datetime=mensagem[3]) for mensagem in mensagens]
        return lista_mensagens_to_db
