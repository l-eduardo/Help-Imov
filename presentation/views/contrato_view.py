import PySimpleGUI as sg
from application.controllers.imoveis_controller import ImoveisController
from infrastructure.repositories.locatarios_repository import LocatariosRepository
from domain.models.locatario import Locatario

# Definição do layout da janela
class TelaContrato:
    def __init__(self, controlador):
        self.__controlador = controlador
        self.__controlador_imovel = ImoveisController(main_controller=controlador)
        self.__locatarios_repository = LocatariosRepository()


    def pega_dados_contrato(self):
        imoveis = self.__controlador_imovel.obter_imoveis_do_banco()
        locatarios = self.__locatarios_repository.get_all()
        nomes_locatarios = [locatario.nome for locatario in locatarios]

        try:
            layout = [
                [sg.Text('Cadastrar Contrato', font=('Any', 18), justification='center', expand_x=True)],
                [sg.Text('Locatário', size=(15, 1), justification='center'),
                 sg.Combo(nomes_locatarios, size=(20, 1), default_value='Selecione', key='locatario')],
                 #sg.Combo(['Locatario 1', 'Locatario 2'], size=(20, 1), default_value='Selecione', key='locatario')],
                [sg.Text('Imóvel', size=(15, 1), justification='center'),
                 sg.Combo(imoveis, size=(20, 1), default_value='Selecione', key='imovel')],
                [sg.Text('Data Início', size=(15, 1), justification='center'), sg.Input(key='data_inicio',
                                                                                        text_color='White',
                                                                                        disabled=True, size=(11, 1)),

                 sg.CalendarButton('Selecionar', size=(9, 1), target='data_inicio', format='%Y/%m/%d')],
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
                    nome_selecionado = values['locatario']
                    # Encontra o objeto locatario com base no nome
                    locatario_selecionado = next((loc for loc in locatarios if loc.nome == nome_selecionado), None)

                    window.close()
                    return values, locatario_selecionado
            # Fechamento da janela
            window.close()
            return None
        except Exception as e:
            print("Erro ao obter dados do contrato", e)
            return None

    def mostra_contratos(self, contratos_listados):

        # Define the table header
        header = ["ID Contrato", "Data Início", "Locatário", "Imóvel", "Status"]

        # Convert the list of dictionaries into a list of lists for the table
        table_data = [[contrato.id, contrato.dataInicio, contrato.locatario.nome, contrato.imovel.endereco,
                       "Ativo" if contrato.estaAtivo else "Encerrado"] for contrato in contratos_listados]

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
            self.window.close()
            return event, values

    def mostra_contrato(self, contrato):
        centrilizedButtons = [sg.Button("Encerrar Contrato"), sg.Button("Voltar")]
        print(contrato)
        layout = [[sg.Text("Detalhes do contrato", font=('Arial', 18, 'bold'), text_color='Black',)],
                  [sg.Text("Data Inicio: ", font=('Arial', 14, 'bold')), sg.Text(contrato.dataInicio, key="dataInicio")],
                  [sg.Text("Data Fim: ", font=('Arial', 14, 'bold')), sg.Text(contrato.dataFim, key="dataFim")],
                  [sg.Text("Locatario: ", font=('Arial', 14, 'bold')), sg.Text(contrato.locatario.nome, key="locatario")],
                  [sg.Text("Imovel: ", font=('Arial', 14, 'bold')), sg.Text(contrato.imovel.endereco, key="imovel")],
                  [sg.Text("Status: ", font=('Arial', 14, 'bold')),
                   sg.Text("Ativo" if contrato.estaAtivo else "Encerrado", key="status")],
                  [sg.Column([centrilizedButtons], justification="center")]]

        window = sg.Window(f"Detalhes do contrato ({contrato.id})",
                           layout, size=(500, 250), font=('bold'))

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Voltar":
                window.close()
                self.__controlador.listar_contrato()
            elif event == "Encerrar Contrato":
                contrato.estaAtivo = False
                #window['status'].update("Encerrado")
                window.close()
                return contrato, event

    def mostra_relacionados_contrato(self, solicitacoes_ocorrencias, contrato_instancia):
        excluir_btn_visivel = False
        if solicitacoes_ocorrencias != [] and solicitacoes_ocorrencias:
            excluir_btn_visivel = True
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
        buttons_layout = [
            sg.Button("Voltar"),
            sg.Button("Adicionar solicitação", key="add_solicitacao"),
            sg.Button("Adicionar ocorrência", key="add_ocorrencia"),
            sg.Button("Selecionar"),
            sg.Button("Excluir", key="Excluir", visible=excluir_btn_visivel)
        ]
        right_button_layout = [
            sg.Button("Solicitações para aprovação", key="Solicitações para aprovação")
        ]
        # Window layout
        layout = [
            [sg.Button("Vistoria Inicial", key="vistoria_inicial"), sg.Button("Contra Vistoria", key="contra_vistoria")],
            [tabela],
            [sg.Column([buttons_layout], expand_x=True),
             sg.Column([right_button_layout], justification='right', expand_x=True)]
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
