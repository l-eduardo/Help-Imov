import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class RelatorioView:
    def __init__(self):
        pass

    def pega_datas(self):
        layout = self.__pegar_datas_layout()

        window = sg.Window("Selecione as datas", layout)

        event, values = window.read()
        window.close()

        return event, values

    def __pegar_datas_layout(self):
        layout = [
            [sg.Text("Data Inicial", expand_x=True),
             sg.Input(key='data_inicial', text_color='Black', disabled=True, size=(20, 1)),
             sg.CalendarButton("Selecionar", target='data_inicial', size=(13, 1))],
            [sg.Text("Data Final", expand_x=True),
             sg.Input(key='data_final',text_color='Black',disabled=True, size=(20, 1)),
             sg.CalendarButton("Selecionar", target='data_final', size=(13, 1))],
            [sg.Button("Gerar Relatorio", key="gerar_relatorio")]
        ]

        return layout

    def mostrar_grafico(self, canvas):
        layout = [
            [sg.Text("Grafico")],
            [sg.Canvas(key="-CANVAS-", size=(800, 800))],
        ]

        window = sg.Window("Grafico", layout, finalize=True, element_justification="center")

        self.__desenhar_figura(window["-CANVAS-"].TKCanvas, canvas)

        while True:
            event, _ = window.read()
            if event == sg.WIN_CLOSED:
                break

        window.close()

    def open_relatorio_menu(self):
        layout = self.__relatorio_menu_layout()

        window = sg.Window(title="Relatorios", layout=layout)

        event,_ = window.read()
        window.close()
        return event

    def __relatorio_menu_layout(self):

        layout = [
            [sg.Column([[sg.Text('Relatorios', font=('Any', 18))]], justification='center')],
            [sg.Text("", size=(0, 1))],
            [sg.Column([[sg.Button("Contratos X Tempo", key="contratos", size=(30, 2))]], justification='center')],
            [sg.Column([[sg.Button("Ocorrencias X Contrato", key="ocorrencias", size=(30, 2))]], justification='center')],
            [sg.Column([[sg.Button("Solicitacoes X Solicitacoes", key="solicitacoes", size=(30, 2))]], justification='center')],
            [sg.Text("", size=(0, 2))],
            [sg.Column([[sg.Button("Voltar", key="voltar")]], justification='center')]
        ]

        return layout

    def __desenhar_figura(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_canvas_agg
