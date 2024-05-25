import PySimpleGUI as sg


class SolicitacaoView:

    def __init__(self, controlador):
        self.__controlador = controlador

    def __layout_nova_solicitacao(self):
        centrilizedButtons = [sg.Button("Registrar", size=(10, 1)), sg.Button("Cancelar", size=(10, 1))]

        layout = [[sg.Text("Titulo ")],
                  [sg.InputText(key="titulo", tooltip="titulo", size=(50, 1), expand_x=True)],
                  [sg.HorizontalSeparator()],
                  [sg.Text("Descrição")],
                  [sg.Multiline(key="descricao", tooltip="descricao", size=(50, 10), no_scrollbar=True,
                                expand_x=True)],
                  [sg.Column([centrilizedButtons], justification="center")]]

        window = sg.Window("Nova Solicitação", layout)

        return window


    def pega_dados_solicitacao(self):
        window = self.__layout_nova_solicitacao()
        event, values = window.read()
        window.close()
        return event, values
