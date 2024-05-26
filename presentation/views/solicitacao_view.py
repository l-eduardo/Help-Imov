import PySimpleGUI as sg
from domain.models.solicitacao import Solicitacao
from domain.enums.status import Status


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

    def editar_solicitacao(self, solicitacao: 'Solicitacao'):

        centrilizedButtons = [sg.Button("Confirmar", key="confirmar_edicao"), sg.Button("Cancelar")]

        layout = [[sg.Text("Titulo "), sg.InputText(key="titulo", tooltip="titulo", size=(50, 1), expand_x=True,
                                                    default_text=solicitacao.titulo)],
                  [sg.Text("Descrição"),
                   sg.Multiline(key="descricao", tooltip="descricao", size=(50, 10), no_scrollbar=True, expand_x=True,
                                default_text=solicitacao.descricao)],
                  [sg.Text("Status"),
                   sg.Combo([Status.ABERTO.value, Status.FECHADO.value], default_value=solicitacao.status.value,
                            key="status")],
                  [sg.Column([centrilizedButtons], justification="center")]]

        window = sg.Window(f"Solicitação: ({solicitacao.id})", layout)
        event, values = window.read()
        window.close()
        return event, values

    def mostra_solicitacao(self, solicitacao: 'Solicitacao'):

        centrilizedButtons =  [sg.Button("Editar", key="editar_solicitacao"),sg.Button("Voltar")]

        layout = [[sg.Text("Detalhes da ocorrencia")],
                  [sg.Text("Titulo: "), sg.Text(solicitacao.titulo, key="titulo")],
                  [sg.Text("Descrição: "), sg.Text(solicitacao.descricao, key="descricao")],
                  [sg.Text("Status: "), sg.Text(solicitacao.status.name, key="status")],
                  [sg.Text("Data de criação: "), sg.Text(solicitacao.data_criacao, key="data_criacao")],
                  [sg.Column([centrilizedButtons], justification="center")]]

        window = sg.Window(f"Detalhes da ocorrencia ({solicitacao.id})", layout)
        event, values = window.read()
        window.close()
        return event, values
