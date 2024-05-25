import PySimpleGUI as sg


class TelaSolicitacao:

    def __init__(self, controlador):
        self.__controlador = controlador


    def pega_dados_solicitacao(self):
        try:
            def valida_entrada(values):
                titulo = values['titulo']
                descricao = values['descricao']
                if len(titulo) > 20:
                    sg.popup_error('O título deve ter no máximo 20 caracteres.')
                    return False
                if len(descricao) > 100:
                    sg.popup_error('A descrição deve ter no máximo 100 caracteres.')
                    return False
                return True

            layout = [
                [sg.Text('Registrar Solicitação', font=('Any', 18), justification='center', expand_x=True)],
                [sg.Text('Título: ', size=(15, 1), justification='center'), sg.InputText(key='titulo', size=(11, 1))],
                [sg.Text('Descrição: ', size=(15, 1), justification='center'), sg.Multiline(key='descricao', size=(40, 5))],
                [sg.Button('Voltar'), sg.Button('Registrar')]
            ]
            # Criação da janela
            self.window = sg.Window('Solicitação', layout, element_justification='center',
                               size=(500, 400), font=('Arial', 18, 'bold'))

            # Loop de eventos
            while True:
                event, values = self.window.read()
                if event == sg.WINDOW_CLOSED or event == 'Voltar':
                    self.window.close()
                    self.__controlador.listar_contrato()
                elif event == 'Registrar':
                    if valida_entrada(values):
                        self.window.close()
                        return values
            # Fechamento da janela
            window.close()
            return None
        except Exception as e:
            print("Erro ao obter dados da solicitação", e)
            return None
