from uuid import UUID
from datetime import datetime
from domain.models.mensagem import Mensagem
from infrastructure.mappers.ImagemInput import ImagemInputMapper
from infrastructure.mappers.DocumentoInput import DocumentoInputMapper
from infrastructure.models.chats import Chats
from infrastructure.models.mensagens import Mensagens
from infrastructure.repositories.user_identity_repository import UserIdentityRepository
from domain.models.chat import Chat


class MensagemInputMapper:
    @staticmethod
    def map_mensagem(mensagem: Mensagens):
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
            lista_mensagens = []
            if not chat:
                 return None
            if chat.mensagens is not None or chat.mensagens != []:
                lista_mensagens = [MensagemInputMapper.map_mensagem(mensagem) for mensagem in chat.mensagens]

            lista_mensagens.sort(key=ChatInputMapper.sort_datetime_criteria)
            chat = Chat(id=chat.id,
                        imagens=ImagemInputMapper.bulk_map_imagens(chat.imagens),
                        documentos=DocumentoInputMapper.bulk_map_documento(chat.documentos),
                        mensagens=lista_mensagens)
            return chat
