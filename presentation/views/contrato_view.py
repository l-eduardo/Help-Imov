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
                [sg.Text('Locatário', size=(15, 1), justification='center'), sg.Combo(['Locatario 1', 'Locatario 2'], size=(20, 1), default_value='Selecione', key='locatario')],
                [sg.Text('Imóvel', size=(15, 1), justification='center'), sg.Combo(imoveis, size=(20, 1), default_value='Selecione', key='imovel')],
                [sg.Text('Data Início', size=(15, 1), justification='center'), sg.Input(key='data_inicio', size=(11, 1)), sg.CalendarButton('Selecionar', target='data_inicio', format='%Y/%m/%d')],
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
                  [sg.Button("Voltar"), sg.Button("Visualizar"), sg.Button("Adicionar"), sg.Button("Selecionar")],]

        # Create the window
        self.window = sg.Window("Contratos", layout, size=(900, 300), resizable=True)

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == "Voltar":
                self.window.close()
                exit(), #revisar e adicionar tela principal do sistema
            self.window.close()
            return event, values



    def mostra_contrato(self, contrato):
        layout = [
            [sg.Text('Dados do Contrato', font=('Any', 18), justification='center', expand_x=True)],
            [sg.Text("Data Início:", size=(15, 1), justification='left'), sg.Text(contrato["dataInicio"])],
            [sg.Text("Data Fim:",  size=(15, 1), justification='left'), sg.Text(contrato["dataFim"])],
            [sg.Text("Locatário:",  size=(20, 1), justification='left'), sg.Text(contrato["locatario"])],
            [sg.Text("Imóvel:",  size=(22, 1), justification='left'), sg.Text(contrato["imovel"])],
            [sg.Button("Voltar")]]

        window = sg.Window('Cadastro de Contrato', layout, element_justification='center',
                           size=(500, 400), font=('Arial', 18, 'bold'))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Voltar":
                window.close()
                self.__controlador.listar_contrato()

    def mostra_relacionados_contrato(self, vistoria_inicial, contra_vistoria, solicitacoes_ocorrencias, contrato_instancia):

        header = ["Tipo", "Título", "Status", "Data Criação"]
        # Convert the list of dictionaries into a list of lists for the table
        table_data = [[dado["tipo"], dado["titulo"], dado["status"], dado["dataCriacao"],] for dado in solicitacoes_ocorrencias]

        vistoria_header = ["Descrição", "Data"]
        vistoria_data = [
            ["Vistoria Inicial", vistoria_inicial['data'] if vistoria_inicial else 'Não disponível'],
            ["Contra-Vistoria", contra_vistoria['data'] if contra_vistoria else 'Não disponível']
        ]

        vistorias_table = sg.Table(vistoria_data, headings=vistoria_header,
                                   auto_size_columns=True,
                                   display_row_numbers=False,
                                   justification='center', key='-VISTORIAS-TABLE-',
                                   num_rows=2,
                                #    vertical_scroll_only=True,
                                   expand_x=True,
                                   expand_y=True,
                                   hide_vertical_scroll=True,
                                   size=(200, 100),

                                   selected_row_colors='#191970 on #add8e6',
                                   enable_events=True,
                                   row_height=25,
                                   pad=(10, 10))
        # Table layout
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
            [vistorias_table],
            [tabela],
            [sg.Button("Voltar"), sg.Button("Adicionar solicitação"), sg.Button("Adicionar ocorrência", key="add_ocorrencia"),
             sg.Button("Selecionar")]
        ]
        # Create the window
        window = sg.Window("Relacionados do contrato", layout, size=(900, 300), resizable=True, finalize=True)

        window['-TABELA-'].bind("<Double-Button-1>", "-DOUBLE-CLICK-")
        window['-VISTORIAS-TABLE-'].bind("<Double-Button-1>", "-DOUBLE-CLICK-")

        while True:
            event, values = self.window.read()
            if event == "Adicionar solicitação":
                self.window.close()
                return self.__controlador.adiciona_solicitacao(contrato_instancia)
            if event == "Voltar":
                self.window.close()
                return
            if event == "Selecionar":
                linha_selecionada = values['-VISTORIAS-TABLE-'][0] if values['-VISTORIAS-TABLE-'] else None
                if linha_selecionada is not None:
                    descricao = vistoria_data[linha_selecionada][0]
                    if descricao == "Vistoria-Inicial":
                        self.__controlador.mostra_vistoria(vistoria_inicial)
                    elif descricao == "Contra-Vistoria":
                        if contra_vistoria:
                            self.__controlador.mostra_vistoria(contra_vistoria)
                        else:
                            criar_contra_vistoria = sg.popup(
                                "Não existe Contra-Vistoria cadastrada",
                                title="Aviso",
                                custom_text=("Criar", "Fechar")
                            )
                            if criar_contra_vistoria == "Criar":
                                self.__controlador.adiciona_vistoria(contrato_instancia)
        self.window.close()

    def mostra_msg(self, msg):
        sg.Popup(msg, font=('Arial', 14, 'bold'), title='Contrato', button_justification='left')




