from typing import List
import PySimpleGUI as sg
from datetime import datetime
from domain.models.usuario import Usuario
from domain.models.chat import Chat
from infrastructure.services.Imagens_Svc import ImagensService
from presentation.components.carrossel_cmpt import Carrossel
from infrastructure.services.Documentos_Svc import DocumentosService
import subprocess, os, platform


class ChatView:

    def mostra_chat(self, usuario_logado: Usuario, chat: Chat, imagens_to_view: List[str], documentos_to_view: List[str]):
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
        imagens_teste = []
        imagens_novas = []
        documentos_novos = []
        print(documentos_to_view)
        while True:
            event, values = window.read(timeout=100)

            if event in ('-SAIR-', sg.WINDOW_CLOSED):
                break

            if event == '-IMAGEM-':
                datetime_atual = datetime.now()
                event_imagem, values_imagem = self.pega_imagem()
                if event_imagem == 'Anexar':
                        try:
                            imagens_teste += values_imagem["imagens"].split(";")
                            imagens_novas = ImagensService.bulk_read(imagens_teste)
                            imagens_invalidas = [imagem for imagem in imagens_novas if not imagem.e_valida()]
                            if imagens_invalidas and len(imagens_invalidas):
                                self.mostra_msg(
                                    "Imagens inválidas. Por favor, selecione imagens "
                                    "com resolucao entre 1280x720 e 1920x1280 pixels!")
                                imagens_novas = [imagem for imagem in imagens_novas if imagem.e_valida()]
                            else:
                                window['-CHAT-'].print(f"{usuario_logado.nome} [{datetime_atual.strftime('%d/%m/%Y %H:%M:%S')}]:",
                                                       text_color="DarkBlue", font='bold')
                                imagens_to_view += imagens_teste
                                window['-CHAT-'].print(f"\nAdiciou um novo anexo \n" + "_" * 126, font='bold')
                                mensagens_novas.append({'usuario': usuario_logado,
                                                        'mensagem': 'Adiciou um novo anexo',
                                                        'datetime': datetime_atual.strftime("%Y-%m-%d %H:%M:%S")})
                        except:
                            sg.popup(
                                "Algo deu errado, tente novamente. \n\nLembre-se que todos os dados são necessários!")

            if event == '-DOCUMENTO-':
                datetime_atual = datetime.now()
                event_documento, value_documento = self.pega_documento()
                if event_documento == "Anexar":
                    documentos_novos = []
                    if value_documento["documento"] != "":
                        for documento in value_documento["documento"].split(";"):
                            documentos_novos.append(DocumentosService.read_file(documento))
                            documentos_to_view.append(documento)

                            window['-CHAT-'].print(
                                f"{usuario_logado.nome} [{datetime_atual.strftime('%d/%m/%Y %H:%M:%S')}]:",
                                text_color="DarkBlue", font='bold')
                            imagens_to_view += imagens_teste
                            window['-CHAT-'].print(f"\nAdiciou um novo anexo \n" + "_" * 126, font='bold')
                            mensagens_novas.append({'usuario': usuario_logado,
                                                    'mensagem': 'Adiciou um novo anexo',
                                                    'datetime': datetime_atual.strftime("%Y-%m-%d %H:%M:%S")})
                    else:
                        self.mostra_msg("Por favor, selecione pelo menos um documento")

            if event == '-ANEXOS-':
                print(chat.imagens)
                self.mostra_anexos(imagens_to_view, documentos_to_view)

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
            # Atualiza a contagem de caracteres e limita a mensagem a 500 caracteres em tempo real
            mensagem_em_edicao = values['-MENSAGEM-']
            self.atualiza_contador_mensagem(mensagem_em_edicao, window)
        window.close()
        return mensagens_novas, imagens_novas, documentos_novos, event

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
        centrilizedButtons = [sg.Button("Anexar", size=(10, 1)), sg.Button("Cancelar", size=(10, 1))]
        layout = [
            [sg.Text("Documento *")],
            [[sg.Input(key='documento', readonly=True, disabled_readonly_background_color='#ECECEC',
                       disabled_readonly_text_color='#545454'),
              sg.FilesBrowse(file_types=(('ALL Files', '*.pdf'),))]],
            [sg.Column([centrilizedButtons], justification="center")]]

        window = sg.Window("Anexar Documento", layout)
        event, values = window.read()
        window.close()
        return event, values

    def mostra_anexos(self, imagens_to_view, documentos_to_view):
        image_index = 0
        layout = [
            [sg.Text("Documentos:", size=(22, 1), justification='left'),
             sg.Button("Abrir", key="abrir_documento")],
            Carrossel.carrossel_layout(imagens_to_view)
        ]
        window = sg.Window('Anexos', layout, element_justification='center',
                           size=(800, 600),
                           font=('Arial', 18, 'bold'))

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Voltar":
                window.close()
                break
            if len(imagens_to_view) > 0:
                window['-COUNT_IMG-'].bind("<Return>", "_Enter")

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
                self.mostra_documento(documentos_to_view)


    def mostra_msg(self, msg):
        sg.Popup(msg, font=('Arial', 14, 'bold'), title='Contrato', button_justification='left')

    def mostra_documento(self, documentos_to_view):
        for documento in documentos_to_view:
            caminho_documento = documento
            try:
                if not os.path.isfile(caminho_documento):
                    raise FileNotFoundError(f"Arquivo não encontrado: {caminho_documento}")

                if platform.system() == 'Darwin':  # macOS
                    teste = subprocess.call(('open', caminho_documento))
                elif platform.system() == 'Windows':  # Windows
                    os.startfile(caminho_documento)
                else:  # linux variants
                    teste = subprocess.call(('xdg-open', caminho_documento))

            except FileNotFoundError as e:
                print(e)
                caminho_documento = os.path.dirname(caminho_documento)
                if platform.system() == 'Darwin':  # macOS
                    teste = subprocess.call(('open', caminho_documento))
                elif platform.system() == 'Windows':  # Windows
                    os.startfile(caminho_documento)
                else:  # linux variants
                    teste = subprocess.call(('xdg-open', caminho_documento))
