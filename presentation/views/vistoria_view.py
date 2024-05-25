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

    def mostra_vistoria(self, vistoria):
        layout = [

            [sg.Text("Vistoria", font=('Any', 18), justification='center', expand_x=True)],
            [sg.Text("Descrição:", size=(15, 1), justification='left'), sg.Text(vistoria["descricao"])],
            [sg.Text("Data de Criação:", size=(15, 1), justification='left'), sg.Text(vistoria["dataCadastro"])],
            [sg.Text("Anexos:", size=(22, 1), justification='left'), sg.Text(vistoria["anexos"])],
            [sg.Button("Voltar")]]

        window = sg.Window('Cadastro de Vistoria', layout, element_justification='center',
                           size=(500, 400), font=('Arial', 18, 'bold'))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Voltar":
                window.close()
                # self.__controlador_contrato.listar_contrato()

    def mostra_msg(self, msg):
        sg.Popup(msg, font=('Arial', 14, 'bold'), title='Vistoria', button_justification='left')
