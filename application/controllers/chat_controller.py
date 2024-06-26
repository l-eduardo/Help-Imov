
import uuid
from sqlalchemy import UUID
from application.controllers.session_controller import SessionController
from domain.models.session import Session
from domain.models.chat import Chat
from domain.models.usuario import Usuario
from infrastructure.services.Documentos_Svc import DocumentosService
from infrastructure.services.Imagens_Svc import ImagensService
from presentation.views.chat_view import ChatView
from infrastructure.repositories.chats_repository import ChatsRepository




class ChatCrontroller:
    def __init__(self):
        self.__chat_view = ChatView()
        self.__chat_repository = ChatsRepository()

    def mostra_chat(self, usuario_logado: Usuario, chat: Chat):
        imagens_to_view = ImagensService.bulk_local_temp_save(chat.imagens)
        documentos_to_view = []
        for documento in chat.documentos:
            documentos_to_view.append(DocumentosService.save_file(documento))

        mensagens_novas, imagens_novas, documentos_novos, event = self.__chat_view.mostra_chat(usuario_logado, chat,
                                                                                                imagens_to_view, documentos_to_view)
        novas_mensagens_obj = chat.incluir_mensagens(mensagens_novas)
        self.__chat_repository.insert_novas_mensagens(chat.id, novas_mensagens_obj)

        #imagens = ImagensService.bulk_read(imagens_novas)
        chat.incluir_imagens(imagens_novas)
        self.__chat_repository.insert_novas_imagens(chat.id, imagens_novas)

        chat.incluir_documentos(documentos_novos)
        self.__chat_repository.insert_novos_documentos(chat.id, documentos_novos)




    def pega_imagem(self):
        pass
