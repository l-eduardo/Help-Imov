import PySimpleGUI as sg
from presentation.components.carrossel_cmpt import Carrossel


# Definição do layout da janela
class TelaVistoria:
    def __init__(self, controlador):
        self.__controlador = controlador

    def pega_dados_vistoria(self):
        layout = [
            [sg.Text("Descrição"), sg.InputText(key="descricao")],
            [sg.Text("Data"), sg.InputText(key="data")],
            [sg.Button("Salvar"), sg.Button("Cancelar")]
        ]

        window = sg.Window("Nova Contra-Vistoria", layout)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Cancelar":
                window.close()
                return None
            if event == "Salvar":
                descricao = values["descricao"]
                data = values["data"]
                # Adicionar validação de dados aqui se necessário
                window.close()
                return {"descricao": descricao, "data": data}


    def __layout_nova_vistoria(self):
        centrilizedButtons = [sg.Button("Registrar", size=(10, 1)), sg.Button("Cancelar", size=(10, 1))]

        layout = [[sg.Text("Descrição")],
                  [sg.Multiline(key="descricao", tooltip="Digite uma descrição...", size=(50, 10), no_scrollbar=True,
                                expand_x=True)],
                  [sg.Text("Imagens")],
                  [[sg.Input(key='imagens'), sg.FilesBrowse()]],
                  [sg.Text("Documento")],
                  [[sg.Input(key='documento'), sg.FilesBrowse()]],
                  [sg.Column([centrilizedButtons], justification="center")]]

        window = sg.Window("Nova Vistoria", layout)

        return window


    def pega_dados_vistoria(self):
        window = self.__layout_nova_vistoria()
        event, values = window.read()
        window.close()
        return event, values


    def mostra_vistoria(self, vistoria, lista_paths_imagens):
        image_index = 0
        layout = [
            [sg.Text("Vistoria", font=('Any', 18), justification='center', expand_x=True)],
            [sg.Text("Descrição:", size=(15, 1), justification='left'), sg.Text(vistoria.descricao)],
            [sg.Text("Caminho do Documento:", size=(22, 1), justification='left'), sg.Text("./Downloads/1716793569984645000_a8c93ce1-d8f9-4607-be5d-f86548c02a0f.pdf")],
            [sg.Button("Voltar"), sg.Button("Excluir"), sg.Button("Editar")],
            Carrossel.carrossel_layout(lista_paths_imagens, image_zoom=1, image_subsample=5)
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


    def mostra_msg(self, msg):
        sg.Popup(msg, font=('Arial', 14, 'bold'), title='Vistoria', button_justification='left')
