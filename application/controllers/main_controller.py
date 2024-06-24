from application.controllers.session_controller import SessionController
from domain.enums.status import Status
from domain.models.chat import Chat
from domain.models.contrato import Contrato
from domain.models.session import Session
from infrastructure.services.Imagens_Svc import ImagensService
from presentation.views.login_view import LoginView
from presentation.views.main_view import MainView
from presentation.views.ocorrencia_view import OcorrenciaView
from application.controllers.usuarios_controller import UsuariosController
from application.controllers.contrato_controller import ContratoController
from application.controllers.imoveis_controller import ImoveisController
from application.controllers.chat_controller import ChatCrontroller
from infrastructure.repositories.user_identity_repository import UserIdentityRepository
from infrastructure.repositories.ocorrencias_repository import OcorrenciasRepository
from infrastructure.repositories.chats_repository import ChatsRepository


class MainController:
    def __init__(self):
        self.__login_view = LoginView()
        self.__main_view = MainView()
        self.__ocorrencia_view: OcorrenciaView = OcorrenciaView()
        self.__session_controller = SessionController()
        self.__usuarios_controller = UsuariosController()
        self.__contrato_controller = ContratoController(self)
        self.__imoveis_controller = ImoveisController(self)
        self.__chat_controller = ChatCrontroller()
        self.user_identity_repository = UserIdentityRepository()
        self.ocorrencias_repository = OcorrenciasRepository()
        self.__chat_repository = ChatsRepository()

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
                self.__set_session(autenticado)
                usuario_atual = self.__session_controller.get_current_user()
                if usuario_atual.user_role == 'Prestador_servico':
                    self.abrir_tela_prestadores()
                    break
                else:
                    self.abrir_tela_inicial()
                    break

            self.__login_view.error_popup("Email ou senha incorretos")

    def __set_session(self, usuario):
        self.__session_controller.get_new_session(usuario.id)
        pass

    def abrir_tela_inicial(self):
        usuario_atual = self.__session_controller.get_current_user()
        is_locatario = usuario_atual.user_role == "Locatario"
        print(usuario_atual.user_role)

        while True:
            event, values = self.__main_view.tela_inicial(disable_usuarios=is_locatario)
            if event == "Sair":
                break
            match event:
                case "usuarios":
                    if not is_locatario:
                        self.__usuarios_controller.lista_usuarios()
                case "imoveis":
                    self.__imoveis_controller.listar_imoveis()
                case "contratos":
                    self.__contrato_controller.listar_contrato()

    @SessionController.inject_session_data
    def abrir_tela_prestadores(self, session: Session = None):
        while True:
            ocorrencias = self.ocorrencias_repository.get_all_to_domain()
            prestador_atual = self.__session_controller.get_current_user()
            ocorrencias_para_tela = []

            for ocorrencia in ocorrencias:
                if prestador_atual.user_id == ocorrencia.prestador_id:
                    ocorrencia_dict = {
                        "tipo": "Ocorrência",
                        "titulo": ocorrencia.titulo,
                        "status": ocorrencia.status.value,
                        "dataCriacao": ocorrencia.data_criacao,
                        "prestador_id": ocorrencia.prestador_id,
                        "entity": ocorrencia
                    }
                    ocorrencias_para_tela.append(ocorrencia_dict)

            event_lista, values_lista = self.__main_view.tela_inicial_prestadores(ocorrencias_para_tela)

            if event_lista == "Sair":
                break

            if event_lista == "-TABELA-DOUBLE-CLICK-":
                while True:
                    entidade = ocorrencias_para_tela[values_lista["-TABELA-"][0]]

                    if entidade["tipo"] == "Ocorrência":
                        imagens_dir = ImagensService.bulk_local_temp_save(entidade["entity"].imagens)
                        mostra_ocorr_event, _ = self.__ocorrencia_view.vw_mostra_ocorrencia(entidade["entity"],
                                                                                            dirs=imagens_dir)

                        if mostra_ocorr_event == "Voltar":
                            break  # Voltar para a tela inicial dos prestadores

                        if mostra_ocorr_event == "editar_ocorrencia":
                            editar_ocorr_events, editar_ocorr_values = self.__ocorrencia_view.vw_editar_ocorrencia(
                                entidade["entity"])
                            if editar_ocorr_events == "confirmar_edicao":
                                prestador_id = editar_ocorr_values.get("prestadores")
                                entidade["entity"].titulo = editar_ocorr_values["titulo"]
                                entidade["entity"].descricao = editar_ocorr_values["descricao"]
                                entidade["entity"].status = Status(editar_ocorr_values["status"])
                                entidade["entity"].prestador_id = prestador_id
                                self.ocorrencias_repository.update(entidade["entity"])

                        elif mostra_ocorr_event == "Chat":
                            chat = entidade["entity"].chat
                            if not isinstance(chat, Chat):
                                chat = entidade["entity"].incluir_chat()
                                self.__chat_repository.insert_chat(chat)

                            usuario_logado_id = session.user_id
                            usuario_logado = self.__usuarios_controller.usuario_by_id(usuario_logado_id)
                            self.__chat_controller.mostra_chat(usuario_logado=usuario_logado, chat=chat)
