from uuid import UUID
from datetime import datetime
from domain.models.mensagem import Mensagem
from infrastructure.mappers.ImagemInput import ImagemInputMapper
from infrastructure.models.chats import Chats
from infrastructure.models.mensagens import Mensagens
from infrastructure.repositories.user_identity_repository import UserIdentityRepository
from domain.models.chat import Chat


class MensagemInputMapper:
    @staticmethod
    def map_chat(mensagem: Mensagens):
            mensagem = Mensagem(id=mensagem.id,
                        usuario=UserIdentityRepository().get_user(user_id=mensagem.usuario_id),
                        mensagem=mensagem.mensagem,
                        datetime=mensagem.datetime)
            return mensagem

class ChatInputMapper:
    @staticmethod
    def sort_datetime_criteria(mensagem):
        mensagem_datetime = datetime.strptime(mensagem.datetime, "%Y-%m-%d %H:%M:%S")
        return mensagem_datetime

    @staticmethod
    def map_chat(chat: Chats):
            lista_mensagens = [MensagemInputMapper.map_chat(mensagem) for mensagem in chat.mensagens]
            lista_mensagens.sort(key=ChatInputMapper.sort_datetime_criteria)
            chat = Chat(id=chat.id,
                        imagens=ImagemInputMapper.bulk_map_imagens(chat.imagens),
                        mensagens=lista_mensagens)
            return chat
