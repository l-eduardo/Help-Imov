from application.controllers.session_controller import SessionController
from infrastructure.repositories.contratos_repository import ContratosRepositories
from presentation.views.login_view import LoginView
from presentation.views.main_view import MainView
from application.controllers.usuarios_controller import UsuariosController
from application.controllers.contrato_controller import ContratoController
from application.controllers.imoveis_controller import ImoveisController


class MainController:
    def __init__(self):
        self.__login_view = LoginView()
        self.__main_view = MainView()
        self.__session_controller = SessionController()
        # self.__usuarios_controller = UsuariosController(self)
        self.__contrato_controller = ContratoController(self)
        self.__imoveis_controller = ImoveisController(self, self)
        self.__main_window = None

    @property
    def contrato_controller(self):
        return self.__contrato_controller

    def run(self):
        while True:
            evento, inputs = self.__login_view.open()

            autenticado = self.__session_controller.autheticate(inputs["email"], inputs["password"])

            if evento == "Cancel" or evento[0] == None:
                break
            if autenticado:
                self.__set_session(autenticado.id)
                self.abrir_tela_inicial()
                break

            self.__login_view.error_popup("Email ou senha incorretos")

    def __set_session(self, id):
        self.__session_controller.get_new_session(id)
        pass

    def abrir_tela_inicial(self):
        while True:
            event, values = self.__main_view.tela_inicial()
            if event == "Voltar":
                break
            match event:
                case "usuarios":
                    pass  # self.__usuarios_controller.lista_usuarios()
                case "imoveis":
                    self.__imoveis_controller.listar_imoveis()
                case "contratos":
                    self.__contrato_controller.listar_contrato()
