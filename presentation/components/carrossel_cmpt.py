import PySimpleGUI as sg


class Carrossel:

    @staticmethod
    def carrossel_layout(lista_paths_imagens, image_zoom=1, image_subsample=2):
        if len(lista_paths_imagens) == 0:
            carrossel_layout = [[sg.HorizontalSeparator()],
                                [sg.Text("Imagens", font=('Any', 18),
                                          justification='center',
                                          expand_x=True)],
                                [sg.Text("Não há imagens registradas ainda.",
                                         font=('Any', 16),
                                         justification='center',
                                         expand_x=True,
                                         text_color='orange')]]
        else:
            carrossel_layout = [[sg.HorizontalSeparator()],
                                [sg.Text("Imagens", font=('Any', 18), justification='center', expand_x=True)],
                                [sg.Button('<', key='-ANT_IMG-',pad=20),
                                    sg.Input("1", key='-COUNT_IMG-', size=(5), justification='right'),
                                    sg.Text(f"/{len(lista_paths_imagens)}", font=('Any', 18), justification='center'),
                                    sg.Button('>', key='-PROX_IMG-',pad=20)],
                                [sg.Image(lista_paths_imagens[0], key='-IMAGE-', subsample=image_subsample, zoom=image_zoom)]]
        return carrossel_layout
