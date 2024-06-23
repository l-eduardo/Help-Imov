import os

import PySimpleGUI as sg

class MainView:
    def tela_inicial(self):
        image_path = os.path.join(os.path.dirname(__file__), '../assets/help-imov-logo.png')

        layout = [
            [sg.Image(filename=image_path, subsample=3 ),
             sg.Text('Help Imov', font=('Any', 18), justification='right')],
            [sg.Text("", size=(0, 1))],
            [sg.Button("Usuários", size=(15, 1), key="usuarios")],
            [sg.Button("Imoveis", size=(15, 1), key="imoveis")],
            [sg.Button("Contratos", key="contratos", size=(15, 1))],
            [sg.Button("Voltar")]
        ]

        window = sg.Window('Help Imov', layout, element_justification='center',
                           size=(700, 600), font=('Arial', 18, 'bold'))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Voltar":
                window.close()
                break
            window.close()
            return event, values
