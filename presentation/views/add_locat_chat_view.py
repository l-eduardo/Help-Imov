from application.controllers.chat_controller import ChatController
from application.controllers.users_controller import UsersController
from domain.models.prestador_servico import PrestadorServico
import PySimpleGUI as sg


class AddLocChatView:
    def __init__(self, prestador_servico: PrestadorServico):
        self.prestador_servico = prestador_servico
        self.user_controller = UsersController
        self.chat_controller = ChatController

    def add_chat_view(self):
        try:
            locatarios = self.user_controller  # TODO implantar aqui o GET all pra buscar todos os locatarios
            layout = [
                [sg.Text('Selecione o locatário para inserir na conversa', font='Helvetica 20')],
                # sg.Combo(locatarios)
                [sg.Button("Voltar")]
            ]

            window = sg.Window(title="Inserir Locatário no Chat", layout=layout, element_justification='center',
                               size=(500, 400), font=('Arial', 18, 'bold'))

            while True:
                event, values = window.read()
                if event == sg.WINDOW_CLOSED or event == 'Voltar':
                    window.close()
                    self.__controlador.listar_contrato()
                elif event == 'Próximo':
                    '''Pega os dados do contrato e chama no return a próxima tela que é a da vistoria'''
                    window.close()
                    return values
            # Fechamento da janela
            window.close()
            return None
        except Exception as e:
            print("Erro ao obter dados do contrato", e)
            return None
