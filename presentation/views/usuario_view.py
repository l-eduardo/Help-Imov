import PySimpleGUI as sg


class UsuarioView:
    def mostra_popup(self, mensagem: str):
        sg.popup(mensagem)

    def lista_usuarios(self, lista_usuarios):
        window = self.__layout_lista_usuarios(lista_usuarios)
        event, values = window.read()
        #window.close()
        return event, values
    
    def pega_dados_usuario(self, permissao):
        window = self.__layout_pega_dados_usuario(permissao)
        event, values = window.read()
        #window.close()
        return event, values

    def __layout_lista_usuarios(self, usuarios_listados):

        header = ["Permissão",
                  "Nome", 
                  "E-mail",  
                  "Data de Nascimento"]

        table_data = [[usuario["permissao"], 
                       usuario["nome"], 
                       usuario["email"], 
                       usuario["data_nascimento"]]
                       for usuario in usuarios_listados]

        # Table layout
        tabela = sg.Table(table_data,
                          headings=header,
                          auto_size_columns=True,
                          display_row_numbers=False,
                          justification='center', key='-TABELA-',
                          selected_row_colors='#191970 on #add8e6',
                          enable_events=False,
                          expand_x=True,
                          expand_y=True,
                          enable_click_events=False,
                          select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                          vertical_scroll_only=False)
        # Window layout
        layout = [[tabela],
                  [sg.Button("Voltar"), 
                   sg.Text("Adicionar usuário: ",
                           pad=((130,0), 0)),
                   sg.Combo(['Administrador', 'Assistente', 'Locatário', 'Prestador de Serviço'],
                             default_value='Escolha a permissão...',
                             enable_events=True,
                             key='-ADC_USUARIO-',
                             readonly=True,
                             pad=((0,130), 0)), 
                   sg.Button("Selecionar")]]
        
        return sg.Window("Lista de Usuários", layout)
    
    def __layout_pega_dados_usuario(self, permissao: str):
        layout = [[sg.Text(f"Novo {permissao}", 
                           expand_x=True)],
                  [sg.Text("Nome: "), 
                   sg.InputText(key="nome", 
                                tooltip="nome do usuário", 
                                size=(50, 1),
                                pad=((72,0),0))],
                  [sg.Text("E-mail: "), 
                   sg.InputText(key="email", 
                                tooltip="e-mail do usuário", 
                                size=(50, 1),
                                pad=((70,0),0))],
                  [sg.Text("Data de Nascimento: "), 
                   sg.InputText(key="data_nascimento", 
                                tooltip="data de nascimento do usuário", 
                                size=(50, 1)),
                   sg.CalendarButton('Selecionar', 
                                     target='data_nascimento', 
                                     format='%Y/%m/%d')],
                   [sg.Button("Cancelar", pad=(10)), sg.Button("Registrar", pad=(10))]]
        
        return sg.Window("Cadastro de Usuário", layout)



# TESTES ============================================================================================================================================
lista_usuarios = [{'permissao': "Administrador", 'nome': "Root", 'email': 'root@root.com', 'data_nascimento': '2000-01-01'},
                  {'permissao': "Administrador", 'nome': "José Carlos", 'email': 'jose.carlos@imov.com', 'data_nascimento': '1989-03-02'},
                  {'permissao': "Assistente", 'nome': "Amanda Silva", 'email': 'amanda.silva@imov.com', 'data_nascimento': '2001-01-01'},
                  {'permissao': "Locatário", 'nome': "Carlos Figueira", 'email': 'carlinho@gmail.com', 'data_nascimento': '1999-01-01'},
                  {'permissao': "Locatário", 'nome': "Suelen Almeida", 'email': 'sueli@hotmail.com', 'data_nascimento': '2002-01-01'},
                  {'permissao': "Prestador de Serviço", 'nome': "Ezequiel Marcos", 'email': 'ezequiel@solucoes.com', 'data_nascimento': '1980-01-01'}]
view = UsuarioView()
# Controler
while True:
    event_lista,values_lista = view.lista_usuarios(lista_usuarios) 
    if event_lista == '-ADC_USUARIO-':
        permissao = values_lista['-ADC_USUARIO-']
        event_usuario,values_usuario = view.pega_dados_usuario(permissao)
        if event_usuario == 'Registrar':
            # Valida campos
            # Se está certo
                # Instancia o usuario
                # Salva no banco
            # Senão: Erro
            usuario = {'permissao': permissao, 
                        'nome': values_usuario['nome'], 
                        'email': values_usuario['email'], 
                        'data_nascimento': values_usuario['data_nascimento']}
            lista_usuarios.append(usuario)
        elif event_usuario == 'Cancelar' or event_usuario == sg.WIN_CLOSED:
            pass

    elif event_lista == sg.WIN_CLOSED:
        break