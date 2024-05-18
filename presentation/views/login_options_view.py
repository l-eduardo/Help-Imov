import PySimpleGUI as sg

class LoginOptionsView:
    def __init__(self):
        self.layout = [
            [sg.Text('Quem esta se autenticando?',
                     font=('Helvetica', 20), justification='center', pad=(10, (20, 30)))],
            [sg.Column([
                [sg.Button('Prestador de Serviço', size=(20, 2))],
                [sg.Button('Assistente', size=(20, 2))],
                [sg.Button('Administrador', size=(20, 2))],
                [sg.Button('Locatario', size=(20, 2))]],
                  vertical_alignment='center', justification='center')]
        ]

        self.window = sg.Window('Login Options', self.layout)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                break
            else:
                print(values)
                print('OK')

        self.window.close()

