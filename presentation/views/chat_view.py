import PySimpleGUI as sg
from datetime import datetime
from domain.models.usuario import Usuario
from domain.models.chat import Chat
from presentation.components.carrossel_cmpt import Carrossel



class ChatView:
    def __init__(self, controlador):
        self.__controlador = controlador

    def mostra_chat(self, usuario_logado: Usuario, chat: Chat, imagens_to_view):
        layout = [
            [sg.Multiline(size=(160, 40), disabled=True, key='-CHAT-')],
            [sg.Multiline(size=(150, 5), key='-MENSAGEM-'),
             sg.Button('Enviar', key="-ENVIAR-")],
            [sg.Button('Anexar Imagem', key="-IMAGEM-"),
             sg.Button('Anexar Documento', key="-DOCUMENTO-"),
             sg.Button('Visualizar Anexos', key="-ANEXOS-"),
             sg.Button('Sair', key="-SAIR-"),
             sg.Text("0/500", key='-CHAR_COUNT-')]
        ]
        window = sg.Window("Chat de Ocorrência", layout, finalize=True)

        # Popula o chat com mensagens do DB
        for mensagem in chat.mensagens:
            datetime_from_db = datetime.strptime(mensagem.datetime, "%Y-%m-%d %H:%M:%S")
            mensagem_datetime = datetime_from_db.strftime("%d/%m/%Y %H:%M:%S")
            window['-CHAT-'].print(f"{mensagem.usuario.nome} [{mensagem_datetime}]:", text_color="DarkBlue", font='bold')
            window['-CHAT-'].print(f"\n{mensagem.mensagem}\n" + "_"*126, font='bold')
        mensagens_novas = []
        imagens_novas = []
        documentos_novos = []
        while True:
            event, values = window.read(timeout=100)

            if event in ('-SAIR-', sg.WINDOW_CLOSED):
                break

            if event == '-IMAGEM-':
                datetime_atual = datetime.now()
                event_imagem, values_imagem = self.pega_imagem()
                print(event_imagem)
                print(values_imagem["imagens"])
                imagens_novas += values_imagem["imagens"].split(";")
                window['-CHAT-'].print(f"{usuario_logado.nome} [{datetime_atual.strftime('%d/%m/%Y %H:%M:%S')}]:",
                                       text_color="DarkBlue", font='bold')
                imagens_to_view += imagens_novas
                window['-CHAT-'].print(f"\nAdiciou um novo anexo \n" + "_" * 126, font='bold')
                mensagens_novas.append({'usuario': usuario_logado,
                                        'mensagem': 'Adiciou um novo anexo',
                                        'datetime': datetime_atual.strftime("%Y-%m-%d %H:%M:%S")})



            if event == '-ANEXOS-':
                print(chat.imagens)
                self.mostra_anexos(imagens_to_view)

            if event == '-ENVIAR-':
                datetime_atual = datetime.now()
                # Garante apenas 500 caracteres e informa usuário caso passou
                if len(values['-MENSAGEM-']) > 500:
                    values['-MENSAGEM-'] = values['-MENSAGEM-'][:500]
                    sg.popup("Uma mensagem é limitada a 500 caracteres! Só foram enviados os primeiros 500 caracteres ao chat")
                window['-CHAT-'].print(f"{usuario_logado.nome} [{datetime_atual.strftime('%d/%m/%Y %H:%M:%S')}]:",
                                       text_color="DarkBlue", font='bold')
                window['-CHAT-'].print(f"\n{values['-MENSAGEM-']}\n" + "_"*126, font='bold')
                mensagens_novas.append({'usuario': usuario_logado,
                                        'mensagem': values['-MENSAGEM-'],
                                        'datetime': datetime_atual.strftime("%Y-%m-%d %H:%M:%S")})
                window['-MENSAGEM-'].update("")
                window['-CHAR_COUNT-'].update("0/500")

                # Atualiza a contagem de caracteres e limita a mensagem a 500 caracteres
                num_char = len(values['-MENSAGEM-'])
                if num_char < 500:
                    window['-CHAR_COUNT-'].update(f"{num_char}/500", text_color='white')
                elif num_char == 500:
                    window['-CHAR_COUNT-'].update("LIMITE DE CARACTERES ATINGIDO! 500/500", text_color='DarkRed')
                else:
                    window['-MENSAGEM-'].update(values['-MENSAGEM-'][:500])
        window.close()
        return mensagens_novas, imagens_novas, documentos_novos, event


    def pega_imagem(self):
        centrilizedButtons = [sg.Button("Anexar", size=(10, 1)), sg.Button("Cancelar", size=(10, 1))]
        layout = [
                  [sg.Text("Imagens *")],
                  [[sg.Input(key='imagens', readonly=True, disabled_readonly_background_color='#ECECEC',
                             disabled_readonly_text_color='#545454'),
                    sg.FilesBrowse(file_types=(('ALL Files', '*.png'),))]],
                  [sg.Column([centrilizedButtons], justification="center")]]

        window = sg.Window("Anexar imagem", layout)
        event, values = window.read()
        window.close()
        return event, values

    def pega_documento(self):
        pass


    def mostra_anexos(self, imagens_to_view):
        image_index = 0
        layout = [
            Carrossel.carrossel_layout(imagens_to_view)
        ]
        window = sg.Window('Anexos', layout, element_justification='center',
                           size=(800, 600),
                           font=('Arial', 18, 'bold'))

        while True:
            event, values = window.read()
            window['-COUNT_IMG-'].bind("<Return>", "_Enter")
            if event == sg.WIN_CLOSED or event == "Voltar":
                window.close()
                break

            if event == "-PROX_IMG-":
                image_index = (image_index + 1) % len(imagens_to_view)
                window['-COUNT_IMG-'].update(f"{image_index + 1}")
                window['-IMAGE-'].update(imagens_to_view[image_index])

            if event == "-ANT_IMG-":
                if image_index == 0:
                    image_index = len(imagens_to_view) - 1
                else:
                    image_index -= 1
                window['-COUNT_IMG-'].update(f"{image_index + 1}")
                window['-IMAGE-'].update(imagens_to_view[image_index])

            if event == '-COUNT_IMG-' + "_Enter":
                try:
                    contador_input = int(values['-COUNT_IMG-'])
                except:
                    contador_input = image_index
                if contador_input > 0 and contador_input <= len(imagens_to_view):
                    image_index = contador_input - 1
                window['-IMAGE-'].update(imagens_to_view[image_index])

            if event == 'abrir_documento':
                #self.abrir_documento(caminho_documento)
                pass
