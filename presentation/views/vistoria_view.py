import PySimpleGUI as sg


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


    def mostra_vistoria(self, vistoria):
        layout = [
            [sg.Text("Vistoria", font=('Any', 18), justification='center', expand_x=True)],
            [sg.Text("Descrição:", size=(15, 1), justification='left'), sg.Text(vistoria.descricao)],
            [sg.Text("Imagens:", size=(15, 1), justification='left'), sg.Text(vistoria.imagens)],
            [sg.Text("Documentos:", size=(22, 1), justification='left'), sg.Text(vistoria.documento)],
            [sg.Button("Voltar"), sg.Button("Excluir"), sg.Button("Editar")]
        ]

        window = sg.Window('Cadastro de Vistoria', layout, element_justification='center',
                           size=(500, 400), font=('Arial', 18, 'bold'))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Voltar":
                window.close()
                break

            if event == "Editar":
                window.close()
                return "editar_vistoria", vistoria

            if event == "Excluir":
                window.close()
                return "excluir_vistoria", vistoria


    def mostra_msg(self, msg):
        sg.Popup(msg, font=('Arial', 14, 'bold'), title='Vistoria', button_justification='left')
