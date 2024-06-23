import PySimpleGUI as sg
from datetime import datetime
from domain.models.usuario import Usuario
from domain.models.chat import Chat


class ChatView:
    def mostra_chat(self, usuario_logado: Usuario, chat: Chat):
        layout = [
            [sg.Multiline(size=(160, 40), disabled=True, key='-CHAT-')],
            [sg.Multiline(size=(150, 5), key='-MENSAGEM-'),
             sg.Button('Enviar', key="-ENVIAR-")],
            [sg.Button('Anexar Imagem', key="-IMAGEM-"), 
             sg.Button('Anexar Documento', key="-DOCUMENTO-"),
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
        while True:
            event, values = window.read(timeout=100)

            if event in ('-SAIR-', sg.WINDOW_CLOSED):
                break

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
        return mensagens_novas
