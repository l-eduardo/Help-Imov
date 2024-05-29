import PySimpleGUI as sg
from application.controllers.imoveis_controller import ImoveisController


# Definição do layout da janela
class TelaContrato:
    def __init__(self, controlador):
        self.__controlador = controlador
        self.__controlador_imovel = ImoveisController()

    def pega_dados_contrato(self):
        imoveis = self.__controlador_imovel.obter_imoveis_do_banco()
        try:
            layout = [
                [sg.Text('Cadastrar Contrato', font=('Any', 18), justification='center', expand_x=True)],
                [sg.Text('Locatário', size=(15, 1), justification='center'),
                 sg.Combo(['Locatario 1', 'Locatario 2'], size=(20, 1), default_value='Selecione', key='locatario')],
                [sg.Text('Imóvel', size=(15, 1), justification='center'),
                 sg.Combo(imoveis, size=(20, 1), default_value='Selecione', key='imovel')],
                [sg.Text('Data Início', size=(15, 1), justification='center'),
                 sg.Input(key='data_inicio', size=(11, 1)),
                 sg.CalendarButton('Selecionar', target='data_inicio', format='%Y/%m/%d')],
                [sg.Button('Voltar'), sg.Button('Próximo')]
            ]
            # Criação da janela
            window = sg.Window('Cadastro de Contrato', layout, element_justification='center',
                               size=(500, 400), font=('Arial', 18, 'bold'))

            # Loop de eventos
            while True:
                event, values = window.read()
                if event == sg.WINDOW_CLOSED or event == 'Voltar':
                    window.close()
                    self.__controlador.listar_contrato()
                elif event == 'Próximo':
                    '''Pega os dados do contrato e chama no return a próxima tela que é a da vistoria'''
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
        header = ["ID Contrato", "Data Início", "Data Fim", "Locatário", "Imóvel"]

        # Convert the list of dictionaries into a list of lists for the table
        table_data = [[contrato["idContrato"], contrato["dataInicio"], contrato["dataFim"], contrato["locatario"],
                       contrato["imovel"]] for contrato in contratos_listados]

        # Table layout
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
        # Window layout
        layout = [[tabela],
                  [sg.Button("Voltar"), sg.Button("Visualizar"), sg.Button("Adicionar"), sg.Button("Selecionar")], ]

        # Create the window
        self.window = sg.Window("Contratos", layout, size=(900, 300), resizable=True)

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == "Voltar":
                self.window.close()
                exit() #revisar e adicionar tela principal do sistema
            self.window.close()
            return event, values

    def mostra_contrato(self, contrato):
        layout = [
            [sg.Text('Dados do Contrato', font=('Any', 18), justification='center', expand_x=True)],
            [sg.Text("Data Início:", size=(15, 1), justification='left'), sg.Text(contrato["dataInicio"])],
            [sg.Text("Data Fim:", size=(15, 1), justification='left'), sg.Text(contrato["dataFim"])],
            [sg.Text("Locatário:", size=(20, 1), justification='left'), sg.Text(contrato["locatario"])],
            [sg.Text("Imóvel:", size=(22, 1), justification='left'), sg.Text(contrato["imovel"])],
            [sg.Button("Voltar")]]

        window = sg.Window('Dados Contrato', layout, element_justification='center',
                           size=(500, 400), font=('Arial', 18, 'bold'))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Voltar":
                window.close()
                self.__controlador.listar_contrato()

    def mostra_relacionados_contrato(self, solicitacoes_ocorrencias, contrato_instancia):

        header = ["Tipo", "Título", "Status", "Data Criação"]
        # Convert the list of dictionaries into a list of lists for the table
        table_data = [[dado["tipo"], dado["titulo"], dado["status"], dado["dataCriacao"], dado] for dado in
                      solicitacoes_ocorrencias]

        tabela = sg.Table(table_data, headings=header,
                          auto_size_columns=True,
                          display_row_numbers=False,
                          justification='center', key='-TABELA-',
                          selected_row_colors='#191970 on #add8e6',
                          enable_events=False,
                          expand_x=True,
                          expand_y=True,
                          hide_vertical_scroll=True,
                          enable_click_events=False,
                          select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                          vertical_scroll_only=False)
        # Window layout
        layout = [
            [sg.Button("Vistoria Inicial", key="vistoria_inicial"), sg.Button("Contra Vistoria", key="contra_vistoria")],
            [tabela],
            [sg.Button("Voltar"),
             sg.Button("Adicionar solicitação",key="add_solicitacao"),
             sg.Button("Adicionar ocorrência",key="add_ocorrencia"),
             sg.Button("Selecionar"), sg.Button("Excluir", key="Excluir")]
        ]
        # Create the window
        window = sg.Window("Relacionados do contrato",layout, size=(900, 300), resizable=True, finalize=True)

        window['-TABELA-'].bind("<Double-Button-1>", "DOUBLE-CLICK-")

        while True:
            event, values = window.read()
            window.close()
            return event, values, contrato_instancia

    def mostra_msg(self, msg):
        sg.Popup(msg, font=('Arial', 14, 'bold'), title='Contrato', button_justification='left')
