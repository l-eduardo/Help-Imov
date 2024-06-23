from uuid import UUID
from domain.models.mensagem import Mensagem
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
    def map_chat(chat: Chats):
            lista_mensagens = [MensagemInputMapper.map_chat(mensagem) for mensagem in chat.mensagens]
            chat = Chat(id=chat.id,
                 mensagens=lista_mensagens)
            return chat