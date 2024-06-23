
import uuid
from sqlalchemy import UUID
from application.controllers.session_controller import SessionController
from domain.models.session import Session
from domain.models.chat import Chat
from domain.models.usuario import Usuario
from presentation.views.chat_view import ChatView
from infrastructure.repositories.chats_repository import ChatsRepository


class ChatCrontroller:
    def __init__(self):
        self.__chat_view = ChatView()
        self.__chat_repository = ChatsRepository()

    def mostra_chat(self, usuario_logado: Usuario, chat: Chat):
        novas_mensagens = self.__chat_view.mostra_chat(usuario_logado, chat)
        print(novas_mensagens)
        novas_mensagens_obj = chat.incluir_mensagens(novas_mensagens)
        self.__chat_repository.insert_novas_mensagens(chat.id, novas_mensagens_obj)
