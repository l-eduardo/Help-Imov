import PySimpleGUI as sg
from application.controllers.controller_contrato import ContratoController

# Definição do layout da janela
class TelaVistoria:
    def __init__(self, controlador):
        self.__controlador = controlador
        self.__controlador_contrato = ContratoController()

    def PegaDadosVistoria(self):
        contratos = self.__controlador_contrato.obter_contratos_do_banco()
        try:
            layout = [
                [sg.Text('Cadastrar Vistoria', font=('Any', 18), justification='center', expand_x=True)],

                [sg.Text('contrato', size=(15, 1), justification='center'),
                 sg.InputCombo([contratos], size=(20, 1), key='contrato')],

                [sg.Text('Descrição', size=(15, 1), justification='center'),
                 sg.InputText( size=(20, 1), default_text = 'Selecione', key='descricao')],

                [sg.Text('Anexos', size=(15, 1), justification='center'),
                 sg.FileBrowse(key='anexos', size=(11, 1))],

                [sg.Button('Voltar'), sg.Button('Finalizar')],

                """ Anexos
                    Contestação: vistoria
                    contrato
                    data criacao
                    descricao
                    eh_contestacao
                    fechada
                    """
            ]
            icone_path = '../assets/help-imov-logo.png'
            # Criação da janela
            window = sg.Window('Cadastro de Vistoria', layout, element_justification='center',
                               size=(500, 400), font=('Arial', 18, 'bold'), icon=icone_path)

            # Loop de eventos
            while True:
                event, values = window.read()
                if event == sg.WINDOW_CLOSED or event == 'Voltar':
                    window.close()
                    self.__controlador.listar_vistoria()
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
            print("Erro ao obter dados do vistoria", e)
            return None

    def mostra_vistorias(self, vistorias_listados):
        # Define the table header
        header = ["Data Início", "Data Fim", "Locatário", "Imóvel"]

        # Convert the list of dictionaries into a list of lists for the table
        table_data = [[vistoria["dataInicio"], vistoria["dataFim"], vistoria["locatario"], vistoria["imovel"]] for
                      vistoria in vistorias_listados]

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
        self.window = sg.Window("Vistorias", layout, size=(900, 300), resizable=True)

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == "Voltar":
                self.window.close()
                exit(), '''REVISAAAAAAAAAARRRR DPS E ADICIONAR A TELA PRINCIPAL'''

            if event == "Selecionar":
                if values["-TABELA-"]:
                    vistoria_selecionado = vistorias_listados[values["-TABELA-"][0]]
                    self.window.close()
                    return self.__controlador.selecionar_vistoria(vistoria_selecionado)
                else:
                    sg.popup("Nenhum vistoria selecionado")
            if event == "Adicionar":
                self.window.close()
                return self.__controlador.inclui_vistoria()
        self.window.close()

    def mostra_vistoria(self, vistoria):
        layout = [
            [sg.Text('Dados do Vistoria', font=('Any', 18), justification='center', expand_x=True)],
            [sg.Text("Data Início:", size=(15, 1), justification='left'), sg.Text(vistoria["dataInicio"])],
            [sg.Text("Data Fim:", size=(15, 1), justification='left'), sg.Text(vistoria["dataFim"])],
            [sg.Text("Locatário:", size=(20, 1), justification='left'), sg.Text(vistoria["locatario"])],
            [sg.Text("Imóvel:", size=(22, 1), justification='left'), sg.Text(vistoria["imovel"])],
            [sg.Button("Voltar"), sg.Button("Solicitações"), sg.Button("Ocorrências")]]

        window = sg.Window('Cadastro de Vistoria', layout, element_justification='center',
                           size=(500, 400), font=('Arial', 18, 'bold'))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Voltar":
                window.close()
                self.__controlador.listar_vistoria()
            if event == "Solicitações":
                pass
            if event == "Ocorrências":
                pass

    def mostra_msg(self, msg):
        sg.Popup(msg, font=('Arial', 14, 'bold'), title='Vistoria', button_justification='left')
