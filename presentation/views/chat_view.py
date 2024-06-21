import PySimpleGUI as sg
from datetime import datetime
from domain.models.usuario import Usuario


class ChatView:
    def mostra_chat(self, usuario_logado: Usuario, mensagens_from_db: list[tuple]):
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
        for mensagem in mensagens_from_db:
            datetime_from_db = datetime.strptime(mensagem[2], "%Y-%m-%d %H:%M:%S")
            mensagem_datetime = datetime_from_db.strftime("%d/%m/%Y %H:%M:%S")
            window['-CHAT-'].print(f"{mensagem[0]} [{mensagem_datetime}]:", text_color="DarkBlue", font='bold')
            window['-CHAT-'].print(f"\n{mensagem[1]}\n" + "_"*126, font='bold')
        
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
                mensagens_novas.append((usuario_logado.nome, values['-MENSAGEM-'], datetime_atual.strftime("%Y-%m-%d %H:%M:%S")))
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


# messages = [("user1", "Bla bla bla", "2010-01-01 10:20:30"), ("user2", "Mu Mu mu", "2012-05-20 15:15:15"), ("user3", "gla gla", "2014-04-01 20:45:01")]

# chat = ChatView()
# messages += chat.mostra_chat("ehobraia", messages)
# chat.mostra_chat("ehobraia", messages)
