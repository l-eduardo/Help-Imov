from application.controllers.session_controller import SessionController
from presentation.views.login_view import LoginView


class MainController:
    def __init__(self):
        self.__login_view = LoginView()
        self.__session_controller = SessionController()

    def run(self):
        while True:
            evento, inputs = self.__login_view.open()

            autenticado = self.__session_controller.autheticate(inputs["email"], inputs["password"])

            if evento == "Cancel" or evento[0] == None:
                break
            if autenticado:
                self.__set_session(autenticado.id)
                break

            self.__login_view.error_popup("Email ou senha incorretos")

    def __set_session(self, id):
        self.__session_controller.get_new_session(id)
        pass
