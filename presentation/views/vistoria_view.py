import PySimpleGUI as sg
import subprocess, os, platform
from presentation.components.carrossel_cmpt import Carrossel


# Definição do layout da janela
class TelaVistoria:
    def __init__(self, controlador):
        self.__controlador = controlador

    def __layout_nova_vistoria(self):
        centrilizedButtons = [sg.Button("Registrar", size=(10, 1)), sg.Button("Cancelar", size=(10, 1))]

        layout = [[sg.Text("Descrição *")],
                  [sg.Multiline(key="descricao", tooltip="Digite uma descrição...", size=(50, 10), no_scrollbar=True,
                                expand_x=True)],
                  [sg.Text("Imagens *")],
                  [[sg.Input(key='imagens', readonly=True, disabled_readonly_background_color='#ECECEC', disabled_readonly_text_color='#545454'),
                    sg.FilesBrowse(file_types=(('ALL Files', '*.png'),))]],
                  [sg.Text("Documento *")],
                  [[sg.Input(key='documento', readonly=True, disabled_readonly_background_color='#ECECEC', disabled_readonly_text_color='#545454'),
                    sg.FilesBrowse(file_types=(('ALL Files', '*.pdf'),))]],
                  [sg.Column([centrilizedButtons], justification="center")]]

        window = sg.Window("Nova Vistoria", layout)

        return window

    def pega_dados_vistoria(self):
        window = self.__layout_nova_vistoria()
        event, values = window.read()
        window.close()
        values["documento"] = values["documento"].split(';')[-1]
        return event, values

    def mostra_vistoria(self, vistoria, lista_paths_imagens, caminho_documento, e_contestacao, user_role):
        image_index = 0

        layout = [
            [sg.Text("Vistoria", font=('Any', 18), justification='center', expand_x=True)],
            [sg.Text("Descrição:", size=(15, 1), justification='left'), sg.Text(vistoria.descricao)],
            [sg.Text("Documentos:", size=(22, 1), justification='left'), sg.Button("Abrir",key="abrir_documento")],
            [sg.Button("Voltar"), sg.Button("Editar",visible=not(user_role == 'Locatario') or e_contestacao),sg.Button("Excluir", visible=e_contestacao)],
            Carrossel.carrossel_layout(lista_paths_imagens)
        ]

        window = sg.Window('Vistoria', layout, element_justification='center',
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
                return "editar_vistoria", vistoria

            if event == "Excluir":
                window.close()
                return "excluir_vistoria", vistoria

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

            if event == 'abrir_documento':
                self.abrir_documento(caminho_documento)

    def mostra_msg(self, msg, nova_vistoria = False):
        return sg.Popup(msg, font=('Arial', 14, 'bold'), title='Vistoria', button_justification='left', custom_text=("Criar","Cancelar") if nova_vistoria else "OK")

    def __layout_editar_vistoria(self, vistoria):

        centrilizedButtons = [sg.Button("Salvar", size=(10, 1)), sg.Button("Cancelar", size=(10, 1))]

        layout = [
            [sg.Text("Descrição *")],
            [sg.Multiline(default_text=vistoria.descricao, key="descricao", tooltip="Digite uma descrição...",
                          size=(50, 10), no_scrollbar=True, expand_x=True)],
            [sg.Column([centrilizedButtons], justification="center")]
        ]

        window = sg.Window("Editar Vistoria", layout)
        return window

    def pega_dados_editar_vistoria(self, vistoria):
        window = self.__layout_editar_vistoria(vistoria)
        event, values = window.read()
        window.close()
        return event, values

    def abrir_documento(self, caminho_documento):
        try:
            if not os.path.isfile(caminho_documento):
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho_documento}")

            if platform.system() == 'Darwin':  # macOS
                teste = subprocess.call(('open', caminho_documento))
            elif platform.system() == 'Windows':  # Windows
                os.startfile(caminho_documento)
            else:  # linux variants
                teste = subprocess.call(('xdg-open', caminho_documento))

            #if teste == 1:
                #raise ValueError("Não há programa padrão para abrir, abrindo diretório")

        except FileNotFoundError as e:
            print(e)
            caminho_documento = os.path.dirname(caminho_documento)
            if platform.system() == 'Darwin':  # macOS
                teste = subprocess.call(('open', caminho_documento))
            elif platform.system() == 'Windows':  # Windows
                os.startfile(caminho_documento)
            else:  # linux variants
                teste = subprocess.call(('xdg-open', caminho_documento))

