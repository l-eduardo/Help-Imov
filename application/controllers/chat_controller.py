from sqlalchemy import UUID
from application.controllers.session_controller import SessionController
from domain.models.session import Session
from infrastructure.repositories.administradores_repository import AdministradoresRepository
from infrastructure.repositories.assistentes_repository import AssistentesRepository
from infrastructure.repositories.locatarios_repository import LocatariosRepository
from infrastructure.repositories.prestadores_servicos_repository import PrestadoresServicosRepository
from presentation.views.chat_view import ChatView
from infrastructure.repositories.chats_repository import ChatsRepository


class ChatCrontroller:
    def __init__(self, id_ocorrencia: UUID):
        self.__chat_view = ChatView()
        self.__chat_repository = ChatsRepository()
        self.__chat = self.__chat_repository.get_by_ocorrencia_id(id_ocorrencia)
    
    @SessionController.inject_session_data
    def mostra_chat(self, session: Session=None):
        dict_roles = {'Administrador': AdministradoresRepository.get_by_id,
                      'Assistente': AssistentesRepository.get_by_id,
                      'Locatario': LocatariosRepository.get_by_id,
                      'PrestadorServico': PrestadoresServicosRepository.get_by_id}
        usuario_logado = dict_roles[session.user_role](session.user_id)
        novas_mensagens = self.__chat_view.mostra_chat(usuario_logado, self.__chat.mensagens)
        self.__chat.mensagens += novas_mensagens
        self.__chat_repository.insert_novas_mensagens(self.__chat.id, novas_mensagens)

