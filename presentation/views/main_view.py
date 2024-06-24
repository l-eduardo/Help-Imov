import os
import PySimpleGUI as sg
from infrastructure.repositories.prestadores_servicos_repository import PrestadoresServicosRepository


class MainView:

    def tela_inicial(self, show_report=False):
        image_path = os.path.join(os.path.dirname(__file__), '../assets/help-imov-logo.png')

        layout = [
            [sg.Image(filename=image_path, subsample=3),
             sg.Text('Help Imov', font=('Any', 18), justification='right')],
            [sg.Text("", size=(0, 1))],
            [sg.Button("Usuários", size=(15, 1), key="usuarios", visible=show_report)],
            [sg.Button("Imoveis", size=(15, 1), key="imoveis")],
            [sg.Button("Contratos", key="contratos", size=(15, 1))],
            [sg.Button("Relatórios", key="relatorios", size=(15, 1), visible=show_report)],
            [sg.Button("Sair")]
        ]

        window = sg.Window('Help Imov', layout, element_justification='center',
                           size=(500, 400), font=('Arial', 18, 'bold'))
        while True:
            event, values = window.read()
            window.close()
            return event, values

    def tela_inicial_prestadores(self, ocorrencias):

        header = ["Tipo", "Título", "Status", "Data Criação"]
        table_data = [[dado["tipo"], dado["titulo"], dado["status"], dado["dataCriacao"], dado] for dado in ocorrencias]

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

        buttons_layout = [
            sg.Button("Sair"),
        ]

        layout = [
            [tabela],
            [sg.Column([buttons_layout], expand_x=True), ]
        ]

        window = sg.Window("Suas ocorrências relacionadas", layout, size=(900, 300), resizable=True, finalize=True)

        window['-TABELA-'].bind("<Double-Button-1>", "DOUBLE-CLICK-")

        while True:
            event, values = window.read()
            window.close()
            return event, values
