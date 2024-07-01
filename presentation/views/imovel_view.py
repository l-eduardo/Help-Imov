import PySimpleGUI as sg
import subprocess, os, platform

from domain.models.imovel import Imovel
from presentation.components.carrossel_cmpt import Carrossel


# Definição do layout da janela
class TelaImovel:
    def __init__(self, controlador):
        self.__controlador = controlador

    def __layout_novo_imovel(self):
        centrilized_buttons = [sg.Button("Registrar", size=(10, 1)), sg.Button("Cancelar", size=(10, 1))]

        layout = [[sg.Text("Codigo *")],
                  [sg.Input(key="codigo", tooltip="digite um codigo", default_text="insira um código numérico válido", size=(50, 10), expand_x=True)],
                  [sg.Text("", key="-ERROR-", size=(50, 1), text_color="red")],
                  [sg.Text("Endereço *")],
                  [sg.Multiline(key="endereco", tooltip="digite o endereço", size=(50, 10), no_scrollbar=True,
                                expand_x=True)],
                  [sg.Text("Imagens *")],
                  [[sg.Input(key='imagens', readonly=True, disabled_readonly_background_color='#ECECEC',
                             disabled_readonly_text_color='#545454'),
                    sg.FilesBrowse(file_types=("ALL Files", "*.png"))]],
                  [sg.Column([centrilized_buttons], justification="center")]]

        window = sg.Window("Novo Imovel", layout)

        return window

    def pega_dados_imovel(self):
        window = self.__layout_novo_imovel()

        event, values = window.read()

        window.close()
        return event, values

    def mostra_imoveis_lista(self, imoveis_listados):
        header = ["Codigo", "Endereço"]

        table_data = [[imovel["codigo"], imovel["endereco"]] for imovel in imoveis_listados]

        tabela = sg.Table(table_data, headings=header,
                          auto_size_columns=True,
                          display_row_numbers=False,
                          justification='center', key='-TABELA-',
                          selected_row_colors='#191970 on #add8e6',
                          enable_events=False,
                          expand_x=True,
                          expand_y=True,
                          enable_click_events=False,
                          select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                          vertical_scroll_only=False)

        layout = [[tabela],
                  [sg.Button("Voltar"), sg.Button("Visualizar"), sg.Button("Adicionar")]]

        # Create the window
        self.window = sg.Window("Imoveis", layout, size=(900, 300), resizable=True)

        while True:
            event, values = self.window.read()
            self.window.close()
            return event, values

    def vw_novo_imovel(self, imovel: 'Imovel', lista_paths_imagens: list[str]):
        window = self.mostra_imovel(imovel, lista_paths_imagens)

        event, values = window.read()

        window.close()
        return event, values

    def mostra_imovel(self, imovel: 'Imovel', lista_paths_imagens: list[str]):
        image_index = 0

        layout = [
            [sg.Text("Imovel", font=('Any', 18), justification='center', expand_x=True)],
            [sg.Text("Codigo:", size=(15, 1), justification='left'), sg.Text(imovel.codigo)],
            [sg.Text("Endereço:", size=(15, 1), justification='left'), sg.Text(imovel.endereco)],
            [sg.Button("Voltar"), sg.Button("Editar"), sg.Button("Excluir")],
            Carrossel.carrossel_layout(lista_paths_imagens)
        ]

        window = sg.Window('Imovel', layout, element_justification='center',
                           size=(800, 600),
                           font=('Arial', 18, 'bold'))

        while True:
            event, values = window.read()
            if '-COUNT_IMG-' in window.AllKeysDict:
                window['-COUNT_IMG-'].bind("<Return>", "_Enter")
            if event == sg.WIN_CLOSED or event == "Voltar":
                window.close()
                return "voltar", imovel

            if event == "Editar":
                window.close()
                return "editar_imovel", imovel

            if event == "Excluir":
                window.close()
                return "excluir_imovel", imovel

            if event == "voltar":
                window.close()

            if event == "-PROX_IMG-":
                image_index = (image_index + 1) % len(lista_paths_imagens)
                window['-COUNT_IMG-'].update(f"{image_index + 1}")
                window['-IMAGE-'].update(lista_paths_imagens[image_index])

            if event == "-ANT_IMG-":
                if image_index == 0:
                    image_index = len(lista_paths_imagens) - 1
                else:
                    image_index -= 1
                window['-COUNT_IMG-'].update(f"{image_index + 1}")
                window['-IMAGE-'].update(lista_paths_imagens[image_index])

            if event == '-COUNT_IMG-' + "_Enter":
                try:
                    contador_input = int(values['-COUNT_IMG-'])
                except:
                    contador_input = image_index
                if contador_input > 0 and contador_input <= len(lista_paths_imagens):
                    image_index = contador_input - 1
                window['-IMAGE-'].update(lista_paths_imagens[image_index])

    def mostra_msg(self, msg):
        sg.Popup(msg, font=('Arial', 14, 'bold'), title='imovel', button_justification='left')

    def __layout_editar_imovel(self, imovel):

        centrilizedButtons = [sg.Button("Salvar", size=(10, 1)), sg.Button("Cancelar", size=(10, 1))]

        layout = [
            [sg.Text("Codigo *")],
            [sg.Input(default_text=imovel.codigo, key="codigo", tooltip="Digite o novo código",
                     size=(50, 10), expand_x=True)],
            [sg.Text("Endereço *")],
            [sg.Multiline(key='endereco', default_text=imovel.endereco, tooltip="Digite a nova descricão"
                          , size=(50, 10), no_scrollbar=True, expand_x=True)],
            [sg.Column([centrilizedButtons], justification="center")],

        ]

        window = sg.Window("Editar imovel", layout)
        return window

    def pega_dados_editar_imovel(self, imovel):
        window = self.__layout_editar_imovel(imovel)
        event, values = window.read()
        window.close()
        return event, values
