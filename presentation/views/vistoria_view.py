import PySimpleGUI as sg


# Definição do layout da janela
class TelaVistoria:
    def __init__(self, controlador):
        self.__controlador = controlador

    def PegaDadosVistoria(self):
        try:
            layout = [
                [sg.Text('Cadastrar Vistoria', font=('Any', 18), justification='center', expand_x=True)],

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
                    descricao = values['descricao']
                    anexos = values['anexos']
                    window.close()
                    return values
            # Fechamento da janela
            window.close()
            return None
        except Exception as e:
            print("Erro ao obter dados da vistoria", e)
            return None

    def mostra_vistoria(self, vistoria):
        layout = [
            [sg.Text("Descricao", font=('Any', 18), justification='center', expand_x=True)],
            [sg.Text("Data de Criação:", size=(15, 1), justification='left'), sg.Text(vistoria["dataCadastro"])],
            [sg.Text("Anexos:", size=(22, 1), justification='left'), sg.Text(vistoria["imovel"])],
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
