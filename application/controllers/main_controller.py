from application.controllers.session_controller import SessionController
from infrastructure.repositories.contratos_repository import ContratosRepositories
from presentation.views.login_view import LoginView
from application.controllers.contrato_controller import ContratoController
from application.controllers.solicitacao_controller import SolicitacaoController

class MainController:
    def __init__(self):
        self.__login_view = LoginView()
        self.__session_controller = SessionController()
        self.__contrato_controller = ContratoController(self)

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
                self.__contrato_controller.listar_contrato()
                break

            self.__login_view.error_popup("Email ou senha incorretos")

    def __set_session(self, id):
        self.__session_controller.get_new_session(id)
        pass

@SessionController.inject_session_data
def teste(id, session=None):
    print("Session: " + session.__str__())
