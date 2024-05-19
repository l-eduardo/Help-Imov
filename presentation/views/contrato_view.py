import PySimpleGUI as sg
from application.controllers.imoveis_controller import ImoveisController


# Definição do layout da janela
class TelaContrato:
    def __init__(self, controlador):
        self.__controlador = controlador
        self.__controlador_imovel = ImoveisController()

    def PegaDadosContrato(self):
        imoveis = self.__controlador_imovel.obter_imoveis_do_banco()
        try:
            layout = [
                [sg.Text('Cadastrar Contrato', font=('Any', 18), justification='center', expand_x=True)],
                [sg.Text('Locatário', size=(15, 1), justification='center'), sg.Combo(['Locatario 1', 'Locatario 2'], size=(20, 1), default_value='Selecione', key='locatario')],
                [sg.Text('Imóvel', size=(15, 1), justification='center'), sg.Combo(imoveis, size=(20, 1), default_value='Selecione', key='imovel')],
                [sg.Text('Data Início', size=(15, 1), justification='center'), sg.Input(key='data_inicio', size=(11, 1)), sg.CalendarButton('Selecionar', target='data_inicio', format='%d-%m-%Y')],
                [sg.Button('Voltar'), sg.Button('Finalizar')]
            ]
            icone_path = '../assets/help-imov-logo.png'
            # Criação da janela
            window = sg.Window('Cadastro de Contrato', layout, element_justification='center',
                               size=(500, 400), font=('Arial', 18, 'bold'), icon=icone_path)

            # Loop de eventos
            while True:
                event, values = window.read()
                if event == sg.WINDOW_CLOSED or event == 'Voltar':
                    break
                elif event == 'Finalizar':
                    locatario = values['locatario']
                    imovel = values['imovel']
                    data_inicio = values['data_inicio']
                    window.close()
                    return values
            # Fechamento da janela
            window.close()
            return None
        except Exception as e:
            print("Erro ao obter dados do contrato", e)
            return None

    def mostra_contratos(self, contratos_listados):
        # Define the table header
        header = ["Data Início", "Data Fim", "Locatário", "Imóvel"]

        # Convert the list of dictionaries into a list of lists for the table
        table_data = [[contrato["dataInicio"], contrato["dataFim"], contrato["locatario"], contrato["imovel"]] for contrato in contratos_listados]

        # Table layout
        tabela = sg.Table(table_data, headings=header,
                          auto_size_columns=True,
                          display_row_numbers=False,
                          justification='center', key='-TABELA-',
                          selected_row_colors='#191970 on #add8e6',
                          enable_events=True,
                          expand_x=True,
                          expand_y=True,
                          enable_click_events=False,
                          select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                          vertical_scroll_only=False)
        # Window layout
        layout = [[tabela],
                  [sg.Button("Voltar"), sg.Button("Selecionar"), sg.Button("Adicionar")]]

        # Create the window
        self.window = sg.Window("Contratos", layout, size=(900, 300), resizable=True)

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == "Voltar":
                break
            if event == "Selecionar":
                if values["-TABELA-"]:
                    contrato_selecionado = [(values["-TABELA-"][0], contratos_listados)]
                    return contrato_selecionado
                else:
                    sg.popup("Nenhum contrato selecionado")
            if event == "Adicionar":
                self.window.close()
                return self.__controlador.inclui_contrato()
        self.window.close()


    def mostra_contrato(self, contrato):
        layout = [[sg.Text("Data Início:"), sg.Text(contrato["dataInicio"])],
                  [sg.Text("Data Fim:"), sg.Text(contrato["dataFim"])],
                  [sg.Text("Locatário:"), sg.Text(contrato["locatario"])],
                  [sg.Text("Imóvel:"), sg.Text(contrato["imovel"])],
                  [sg.Button("Ok")]]

        window = sg.Window("Detalhes do Contrato", layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Ok":
                break
        window.close()


    def mostra_msg(self, msg):
        sg.Popup(msg, font=('Arial', 14, 'bold'), title='Contrato', button_justification='left')



if __name__ == "__main__":
    controlador = None  # Substitua pelo seu controlador
    tela = TelaContrato(controlador)
    dados_contrato = tela.PegaDadosContrato()

    contratos_listados = [
        {"dataInicio": "01/01/2021", "dataFim": "31/12/2021", "locatario": "João", "imovel": "Apartamento 101"},
        {"dataInicio": "15/02/2021", "dataFim": "14/02/2022", "locatario": "Maria", "imovel": "Casa 202"}
    ]
    tela.mostra_contratos(contratos_listados)

    print(dados_contrato)


