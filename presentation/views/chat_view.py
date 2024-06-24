from typing import List
import PySimpleGUI as sg
from datetime import datetime
from domain.models.usuario import Usuario
from domain.models.chat import Chat
from presentation.components.carrossel_cmpt import Carrossel


class ChatView:

    def mostra_chat(self, usuario_logado: Usuario, chat: Chat, imagens_to_view: List[str]):
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
        mensagens_novas_buffer = []
        imagens_novas_buffer = []
        documentos_novos_buffer = []
        while True:
            event, values = window.read(timeout=100)

            if event in ('-SAIR-', sg.WINDOW_CLOSED):
                break

            if event == '-IMAGEM-':
                datetime_atual = datetime.now()
                event_imagem, values_imagem = self.pega_imagem()
                if event_imagem == 'Anexar':
                    imagens_selecionadas = values_imagem["imagens"].split(";")
                    imagens_novas_buffer += imagens_selecionadas
                    imagens_to_view += imagens_selecionadas
                    window['-CHAT-'].print(f"{usuario_logado.nome} [{datetime_atual.strftime('%d/%m/%Y %H:%M:%S')}]:",
                                        text_color="DarkBlue", font='bold')
                    window['-CHAT-'].print(f"\nAdicionou um novo anexo \n" + "_" * 126, font='bold')
                    self.adiciona_mensagem_buffer(usuario = usuario_logado,
                                                    mensagem = 'Adicionou um novo anexo',
                                                    datetime_formatado = datetime_atual.strftime("%Y-%m-%d %H:%M:%S"),
                                                    lista = mensagens_novas_buffer)
                elif event_imagem in ('Cancelar',sg.WIN_CLOSED):
                    sg.popup("Nenhuma imagem foi adicionada!")

            if event == '-ANEXOS-':
                print(chat.imagens)
                self.mostra_anexos(imagens_to_view)
        
            if event == '-ENVIAR-':
                datetime_atual = datetime.now()
                nova_mensagem = values['-MENSAGEM-']
                if self.mensagem_vazia(nova_mensagem):
                    self.mostra_popup("O corpo da mensagem está vazio. Escreva algo primeiro!")
                else:
                    # Garante apenas 500 caracteres sobreescrevendo o corpo da mensagem ao enviar
                    if self.mensagem_ultrapassou_limite(nova_mensagem):
                        nova_mensagem = nova_mensagem[:500]
                        self.mostra_popup("A mensagem ultrapassou o limite de caracteres, apenas os primeiros 500 foram enviados!")
                    # Escreve mensagem na tela
                    window['-CHAT-'].print(f"{usuario_logado.nome} [{datetime_atual.strftime('%d/%m/%Y %H:%M:%S')}]:",
                                        text_color="DarkBlue", font='bold')
                    window['-CHAT-'].print(f"\n{nova_mensagem}\n" + "_"*126, font='bold')
                    # Adiciona mensagem à lista mensagens_novas_buffer para depois instanciar
                    self.adiciona_mensagem_buffer(usuario = usuario_logado,
                                                  mensagem = nova_mensagem,
                                                  datetime_formatado = datetime_atual.strftime("%Y-%m-%d %H:%M:%S"),
                                                  lista = mensagens_novas_buffer)
                    window['-MENSAGEM-'].update("")
                    window['-CHAR_COUNT-'].update("0/500")

            # Atualiza a contagem de caracteres e limita a mensagem a 500 caracteres em tempo real
            mensagem_em_edicao = values['-MENSAGEM-']
            self.atualiza_contador_mensagem(mensagem_em_edicao, window)
        window.close()
        return mensagens_novas_buffer, imagens_novas_buffer, documentos_novos_buffer, event

    def mensagem_vazia(self, mensagem: str):
        if len(mensagem) == 0:
            return True
        else:
            return False

    def mensagem_ultrapassou_limite(self, mensagem: str):
        if len(mensagem) > 500:
            return True
        else:
            return False
        
    def atualiza_contador_mensagem(self, mensagem_em_edicao: str, window: sg.Window):
        quantidade_caracteres = len(mensagem_em_edicao)
        if quantidade_caracteres < 500:
            window['-CHAR_COUNT-'].update(f"{quantidade_caracteres}/500", text_color='white')
        elif quantidade_caracteres == 500:
            window['-CHAR_COUNT-'].update("LIMITE DE CARACTERES ATINGIDO! 500/500", text_color='DarkRed')
        else:
            window['-MENSAGEM-'].update(mensagem_em_edicao[:500])

    def adiciona_mensagem_buffer(self, usuario: Usuario, mensagem: str, datetime_formatado: str, lista: List):
        lista.append({'usuario': usuario,
                      'mensagem': mensagem,
                      'datetime': datetime_formatado})
    
    def mostra_popup(self, texto: str):
        sg.popup(texto)

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
