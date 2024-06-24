import os

import PySimpleGUI as sg

class MainView:
    def tela_inicial(self, show_report=False):
        image_path = os.path.join(os.path.dirname(__file__), '../assets/help-imov-logo.png')

        layout = [
            [sg.Image(filename=image_path, subsample=3 ),
             sg.Text('Help Imov', font=('Any', 18), justification='right')],
            [sg.Text("", size=(0, 1))],
            [sg.Button("Usuários", size=(15, 1), key="usuarios")],
            [sg.Button("Imoveis", size=(15, 1), key="imoveis")],
            [sg.Button("Contratos", key="contratos", size=(15, 1))],
            [sg.Button("Relatórios", key="relatorios", size=(15, 1), visible=show_report)],
            [sg.Button("Voltar", key="voltar")]
        ]

        window = sg.Window('Help Imov', layout, element_justification='center',
                           size=(500, 400), font=('Arial', 18, 'bold'))
        while True:
            event, values = window.read()
            window.close()
            return event, values
