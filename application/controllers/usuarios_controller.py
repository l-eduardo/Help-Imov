from presentation.views.usuario_view import UsuarioView
from infrastructure.repositories.administradores_repository import AdministradoresRepository
from infrastructure.repositories.assistentes_repository import AssistentesRepository
from infrastructure.repositories.locatarios_repository import LocatariosRepository
from infrastructure.repositories.prestadores_servicos_repository import PrestadoresServicosRepository


class UsuariosController:
    def __init__(self):
        self.__tela_usuarios = UsuarioView()
        self.__administradores = []
        self.__assistentes = []
        self.__locatarios = []
        self.__prestadores_servicos = []
        self.__administradores_repository = AdministradoresRepository()
        self.__assistentes_repository = AssistentesRepository()
        self.__locatarios_repository = LocatariosRepository
        self.__prestadores_servicos_repository = PrestadoresServicosRepository

    def lista_usuarios(self):
        pass

    def obter_usuarios_do_banco(self) -> list:
        self.__administradores = self.__administradores_repository.get_all()
        self.__assistentes = self.__assistentes_repository.get_all()
        self.__locatarios = self.__locatarios_repository.get_all()
        self.__prestadores_servicos = self.__prestadores_servicos_repository.get_all()
    

