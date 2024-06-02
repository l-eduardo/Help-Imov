import PySimpleGUI as sg

from domain.enums.status import Status
from domain.models.ocorrencia import Ocorrencia

class OcorrenciaView:
    def mostra_popup(self, mensagem: str):
        sg.popup(mensagem)

    def vw_nova_ocorrencia(self):
        window = self.__add_ocorrencia_layout()

        event, values = window.read()

        values['imagens'] = values['imagens'].split(';') if values['imagens'] else []

        window.close()
        return event, values



    def vw_editar_ocorrencia(self, ocorrencia: 'Ocorrencia'):
        window = self.__edit_ocorrencia_layout(ocorrencia)

        event, values = window.read()

        window.close()
        return event, values

    def __edit_ocorrencia_layout(self, ocorrencia: 'Ocorrencia'):
        centrilizedButtons =  [sg.Button("Confirmar", key="confirmar_edicao"),sg.Button("Cancelar")]

        layout = [[sg.Text("Titulo "), sg.InputText(key="titulo", tooltip="titulo", size=(50,1), expand_x=True, default_text=ocorrencia.titulo)],
                  [sg.Text("Descrição"), sg.Multiline(key="descricao", tooltip="descricao", size=(50,10), no_scrollbar=True, expand_x=True, default_text=ocorrencia.descricao)],
                  [sg.Text("Status"), sg.Combo([Status.ABERTO.value, Status.FECHADO.value], default_value=ocorrencia.status.value, key="status")],
                  [sg.Column([centrilizedButtons], justification="center")]]



        window = sg.Window(f"Help imov - Detalhes da ocorrencia ({ocorrencia.id})", layout)

        return window

    def vw_mostra_ocorrencia(self, ocorrencia: 'Ocorrencia', dirs: list[str]):
        window = self.__show_details_layout(ocorrencia, dirs)

        event, values = window.read()

        window.close()
        return event, values

    def __show_details_layout(self, ocorrencia: 'Ocorrencia', dirs: list[str]):

        centrilizedButtons =  [sg.Button("Editar", key="editar_ocorrencia"),sg.Button("Voltar")]

        layout = [[sg.Text("Detalhes da ocorrencia")],
              [sg.Text("Titulo: "), sg.Text(ocorrencia.titulo, key="titulo")],
              [sg.Text("Descrição: "), sg.Text(ocorrencia.descricao, key="descricao")],
              [sg.Text("Status: "), sg.Text(ocorrencia.status.name, key="status")],
              [sg.Text("Data de criação: "), sg.Text(ocorrencia.data_criacao, key="data_criacao")],
              [sg.Text("Imagens: ")],
              [sg.Image(filename=dir, size=(200,133), subsample=5, zoom=1) for dir in dirs],
              [sg.Column([centrilizedButtons], justification="center")]]

        window = sg.Window(f"Help imov - Detalhes da ocorrencia ({ocorrencia.id})", layout)

        return window

    def __add_ocorrencia_layout(self):
        centrilizedButtons = [sg.Button("Salvar", size=(10,1)), sg.Button("Cancelar", size=(10,1))]

        layout = [[sg.Text("Titulo ")],
                  [sg.InputText(key="titulo", tooltip="titulo", size=(50,1), expand_x=True)],
                  [sg.HorizontalSeparator()],
                  [sg.Text("Descrição")],
                  [sg.Multiline(key="descricao", tooltip="descricao", size=(50,10), no_scrollbar=True, expand_x=True)],
                  [[sg.Input(key='imagens'), sg.FilesBrowse(initial_folder="./", file_types=(("Imagens", "*.png"),), tooltip="Selecione imagens da ocorrencia...")]],
                  [sg.Column([centrilizedButtons], justification="center")]]


        window = sg.Window("Help imov - Nova ocorrencia", layout)

        return window
