import PySimpleGUI as sg

class OcorrenciaView:
    def __add_ocorrencia_layout(self):
        centrilizedButtons = [sg.Button("Salvar", size=(10,1)), sg.Button("Cancelar", size=(10,1))]

        layout = [[sg.Text("Titulo ")],
                  [sg.InputText(key="titulo", tooltip="titulo", size=(50,1), expand_x=True)],
                  [sg.HorizontalSeparator()],
                  [sg.Text("Descrição")],
                  [sg.Multiline(key="descricao", tooltip="descricao", size=(50,10), no_scrollbar=True, expand_x=True)],
                  [sg.Column([centrilizedButtons], justification="center")]]


        window = sg.Window("Help imov - Nova ocorrencia", layout)

        return window

    def vw_nova_ocorrencia(self):
        window = self.__add_ocorrencia_layout()

        event, values = window.read()

        window.close()
        return event, values
