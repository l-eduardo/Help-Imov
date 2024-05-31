import PySimpleGUI as sg
import subprocess, os, platform
from presentation.components.carrossel_cmpt import Carrossel


# Definição do layout da janela
class TelaImovel:
    def __init__(self, controlador):
        self.__controlador = controlador

    def __layout_novo_imovel(self):
        centrilized_buttons = [sg.Button("Registrar", size=(10, 1)), sg.Button("Cancelar", size=(10, 1))]

        layout = [[sg.Text("Codigo")],
                  [sg.Text(key="codigo", tooltip="digite um codigo", size=(50, 10), expand_x=True)],
                  [sg.Text("Endereço")],
                  [sg.Multiline(key="endereço", tooltip="digite o endereço", size=(50, 10), no_scrollbar=True,
                                expand_x=True)],
                  [sg.Text("Imagens")],
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
                  [sg.Button("Voltar"), sg.Button("Visualizar"), sg.Button("Adicionar"), sg.Button("Selecionar")], ]

        # Create the window
        self.window = sg.Window("Imoveis", layout, size=(900, 300), resizable=True)

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == "Voltar":
                self.window.close()
                exit()  # revisar e adicionar tela principal do sistema
            self.window.close()
            return event, values
    def mostra_imovel(self, imovel, lista_paths_imagens):
        image_index = 0

        layout = [
            [sg.Text("Imovel", font=('Any', 18), justification='center', expand_x=True)],
            [sg.Text("Codigo:", size=(15, 1), justification='left'), sg.Text(imovel.codigo)],
            [sg.Text("Endereço:", size=(15, 1), justification='left'), sg.Multiline(imovel.endereco)],
            [sg.Button("Voltar"), sg.Button("Editar"), sg.Button("Excluir")],
            Carrossel.carrossel_layout(lista_paths_imagens)
        ]

        window = sg.Window('Imovel', layout, element_justification='center',
                           size=(800, 600),
                           font=('Arial', 18, 'bold'))

        while True:
            event, values = window.read()
            window['-COUNT_IMG-'].bind("<Return>", "_Enter")
            if event == sg.WIN_CLOSED or event == "Voltar":
                window.close()
                break

            if event == "Editar":
                window.close()
                return "editar_imovel", imovel

            if event == "Excluir":
                window.close()
                return "excluir_imovel", imovel

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
            [sg.Text("Codigo")],
            [sg.Text(text=imovel.descricao, key="codigo", tooltip="Digite uma descrição...",
                          size=(50, 10), expand_x=True)],
            [sg.Text("Endereço")],
            [sg.Text(key='endereco', text=imovel.endereco, tooltip="Digite uma descrição...")],
            [sg.Text("Imagens")],
            [sg.Input(key='imagens', readonly=True, disabled_readonly_background_color='#ECECEC',
                      disabled_readonly_text_color='#545454'),
             sg.FilesBrowse(file_types=("ALL Files", "*.png"))]
        ]

        window = sg.Window("Editar imovel", layout)
        return window

    def pega_dados_editar_imovel(self, imovel):
        window = self.__layout_editar_imovel(imovel)
        event, values = window.read()
        window.close()
        return event, values

    def abrir_documento(self, caminho_documento):
        try:
            if platform.system() == 'Darwin':  # macOS
                teste = subprocess.call(('open', caminho_documento))
            elif platform.system() == 'Windows':  # Windows
                teste = os.startfile(caminho_documento)
            else:  # linux variants
                teste = subprocess.call(('xdg-open', caminho_documento))
            if teste == 1:
                raise ValueError("Não há programa padrão para abrir, abrindo diretório")
        except:
            caminho_documento = caminho_documento.replace(caminho_documento.split('/')[-1], "")
            if platform.system() == 'Darwin':  # macOS
                teste = subprocess.call(('open', caminho_documento))
            elif platform.system() == 'Windows':  # Windows
                teste = os.startfile(caminho_documento)
            else:  # linux variants
                teste = subprocess.call(('xdg-open', caminho_documento))