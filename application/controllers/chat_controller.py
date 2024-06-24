
import uuid
from sqlalchemy import UUID
from application.controllers.session_controller import SessionController
from domain.models.session import Session
from domain.models.chat import Chat
from domain.models.usuario import Usuario
from infrastructure.services.Imagens_Svc import ImagensService
from presentation.views.chat_view import ChatView
from infrastructure.repositories.chats_repository import ChatsRepository




class ChatCrontroller:
    def __init__(self):
        self.__chat_view = ChatView()
        self.__chat_repository = ChatsRepository()

    def mostra_chat(self, usuario_logado: Usuario, chat: Chat):
        imagens_to_view = ImagensService.bulk_local_temp_save(chat.imagens)
        mensagens_novas, imagens_novas, documentos_novos, event = self.__chat_view.mostra_chat(usuario_logado, chat,
                                                                                                imagens_to_view)
        print(imagens_novas)
        novas_mensagens_obj = chat.incluir_mensagens(mensagens_novas)
        self.__chat_repository.insert_novas_mensagens(chat.id, novas_mensagens_obj)

        imagens = ImagensService.bulk_read(imagens_novas)
        chat.incluir_imagens(imagens)
        self.__chat_repository.insert_novas_imagens(chat.id, imagens)




    def pega_imagem(self):
        pass
