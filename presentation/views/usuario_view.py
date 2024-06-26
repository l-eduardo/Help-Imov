from typing import List
import PySimpleGUI as sg
from domain.models.usuario import Usuario

class UsuarioView:
    def mostra_popup(self, mensagem: str, confirmacao: bool = False):
        if confirmacao:
            return sg.popup_yes_no(mensagem)
        else:
            sg.popup(mensagem)

    def lista_usuarios(self, lista_usuarios: List[Usuario], e_admin: bool):
        window = self.__layout_lista_usuarios(lista_usuarios, e_admin)
        event, values = window.read()
        window.close()
        return event, values

    def pega_dados_usuario(self, permissao, usuario: Usuario= None, edit_mode: bool = False):
        window = self.__layout_pega_dados_usuario(permissao, usuario = usuario, edit_mode = edit_mode)
        event, values = window.read()
        window.close()
        return event, values
    
    def mostra_usuario(self, usuario: Usuario):
        window = self.__layout_mostra_usuario(usuario, usuario.__class__.__name__)
        event, values = window.read()
        window.close()
        return event, values

    def __layout_lista_usuarios(self, usuarios_listados: List[Usuario], e_admin: bool):

        header = ["Permissão",
                  "Nome", 
                  "E-mail",  
                  "Data de Nascimento"]

        table_data = [[usuario.__class__.__name__, 
                       usuario.nome, 
                       usuario.email, 
                       usuario.data_nascimento]
                       for usuario in usuarios_listados]
        
        permissoes_editaveis = ['Administrador', 'Assistente', 'Locatario', 'PrestadorServico']\
                                 if e_admin else ['Locatario', 'PrestadorServico']

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
                  [sg.Button("Voltar", key="-VOLTAR-"), 
                   sg.Text("Adicionar usuário: ",
                           pad=((130,0), 0)),
                   sg.Combo(permissoes_editaveis,
                             default_value='Escolha a permissão...',
                             enable_events=True,
                             key='-ADC_USUARIO-',
                             readonly=True,
                             pad=((0,130), 0)), 
                   sg.Button("Selecionar", key='-MOSTRA_USUARIO-')]]
        
        return sg.Window("Lista de Usuários", layout)
    
    def __layout_pega_dados_usuario(self, permissao: str, usuario: Usuario = None, edit_mode: bool = False):
        if edit_mode:
            window_title = "Edição de Usuário"
            title = f"Editando usuário {usuario.nome} - Permissão: {permissao}"
            nome_usuario = usuario.nome
            email_usuario = usuario.email
            senha_usuario = '******'
            data_nascimento = usuario.data_nascimento
            if usuario.__class__.__name__ == 'Locatario':
                celular_usuario = usuario.celular
            elif usuario.__class__.__name__ == 'PrestadorServico':
                empresa_usuario = usuario.empresa
                especialidade_usuario = usuario.especialidade
        else:
            window_title = "Cadastro de Usuário"
            title = f"Novo {permissao}"
            nome_usuario = ''
            email_usuario = ''
            senha_usuario = ''
            data_nascimento = ''
            celular_usuario = ''
            empresa_usuario = ''
            especialidade_usuario = ''

        layout_padrao = [[sg.Text(title, 
                           expand_x=True)],
                          [sg.Text("Nome: "), 
                            sg.InputText(default_text=nome_usuario,
                                            key="nome", 
                                            tooltip="nome do usuário", 
                                            size=(50, 1),
                                            pad=((72,0),5))],
                          [sg.Text("E-mail: "), 
                            sg.InputText(default_text=email_usuario,
                                            key="email",
                                            tooltip="e-mail do usuário", 
                                            size=(50, 1),
                                            pad=((70,0),5))],
                          [sg.Text("Senha: "), 
                            sg.InputText(default_text=senha_usuario,
                                            key="senha", 
                                            tooltip="senha do usuário", 
                                            size=(50, 1),
                                            pad=((69,0),5),
                                            password_char='*')],
                          [sg.Text("Data de Nascimento: "), 
                            sg.InputText(default_text=data_nascimento,
                                            readonly = True,
                                            disabled_readonly_background_color='#ECECEC', 
                                            disabled_readonly_text_color='#545454',
                                            key="data_nascimento", 
                                            tooltip="data de nascimento do usuário", 
                                            size=(50, 1)),
                            sg.CalendarButton('Selecionar', 
                                                target='data_nascimento', 
                                                format='%Y-%m-%d')]]
        if permissao == 'Locatario':
            layout_padrao.append([sg.Text("Celular: "), 
                                   sg.InputText(default_text=celular_usuario,
                                                key="celular", 
                                                tooltip="celular", 
                                                size=(50, 1),
                                                pad=((66,0),5))])
        elif permissao == 'PrestadorServico':
            layout_padrao.append([[sg.Text("Especialidade: "), 
                                   sg.InputText(default_text=especialidade_usuario,
                                                key="especialidade", 
                                                tooltip="especialidade", 
                                                size=(50, 1),
                                                pad=((34,0),5))],
                                 [sg.Text("Empresa: "), 
                                   sg.InputText(default_text=empresa_usuario,
                                                key="empresa", 
                                                tooltip="empresa", 
                                                size=(50, 1),
                                                pad=((58,0),5))]])
        layout_completo = [[layout_padrao],
                           [sg.Button("Cancelar", key="-CANCELAR-", pad=(10)), 
                            sg.Button("Registrar", key="-REGISTRAR-", pad=(10))]]

        return sg.Window(window_title, layout_completo)
    
    def __layout_mostra_usuario(self, usuario: Usuario, permissao = str):
        layout_padrao = [[sg.Text(f"Permissão: {permissao}", 
                           expand_x=True)],
                          [sg.Text("Nome: "), 
                           sg.Text(usuario.nome)],
                          [sg.Text("E-mail: "), 
                           sg.Text(usuario.email)],
                          [sg.Text("Data de Nascimento: "),
                           sg.Text(usuario.data_nascimento)]]
        if permissao == 'Locatario':
            layout_padrao.append([sg.Text("Celular: "), 
                                   sg.Text(usuario.celular)])
        elif permissao == 'PrestadorServico':
            layout_padrao.append([[sg.Text("Especialidade: "), 
                                   sg.Text(usuario.especialidade)],
                                 [sg.Text("Empresa: "), 
                                   sg.Text(usuario.empresa)]])
        layout_completo = [[layout_padrao],
                           [sg.Button("Voltar", key="-VOLTAR-", pad=(10)), 
                            sg.Button("Editar", key="-EDITAR-", pad=(10)),
                            sg.Button("Excluir", key="-EXCLUIR-", pad=(10))]]

        return sg.Window("Dados do Usuário", layout_completo)

