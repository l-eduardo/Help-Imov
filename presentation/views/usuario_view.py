from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from typing import List
from kivy.uix.widget import Widget
from domain.models.administrador import Administrador
from domain.models.assistente import Assistente
from domain.models.locatario import Locatario
from domain.models.prestador_servico import PrestadorServico


class TelaInicial(BoxLayout):
    def __init__(self, usuarios, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Cor de fundo (cinza claro)
            self.bg = Rectangle(size=self.size, pos=self.pos)

        # Atualizar o tamanho do retângulo ao redimensionar
        self.bind(size=self.update_bg, pos=self.update_bg)

        # Layout do topo da tela
        topo = BoxLayout(size_hint=(1, 0.1), padding=(10,10))

        logo = Image(source='assets/help-imov-logo.png')

        titulo = Label(text='Usuários',
                       halign='center',
                       valign='middle',
                       color=(0, 0, 0, 1),
                       font_size='24sp')

        adicionar_btn = Button(text="Adicionar")

        adicionar_btn.bind(on_release=self.adicionar_usuario)

        topo.add_widget(logo)
        topo.add_widget(titulo)
        topo.add_widget(adicionar_btn)

        self.add_widget(topo)

        scroll_view = ScrollView(size_hint=(1, 0.8))
        lista = BoxLayout(orientation='vertical', size_hint_y=None)
        lista.bind(minimum_height=scroll_view.setter('height'))

        # Lista de imóveis cadastrados
        for usuario in usuarios:
            lista.add_widget(self.criar_linha_usuario(usuario))

        scroll_view.add_widget(lista)
        self.add_widget(scroll_view)

        # Botão para voltar
        voltar_btn = Button(text="Voltar", size_hint=(1, 0.1))
        self.add_widget(voltar_btn)

    # renderiza a lista para cada novo usuario criado
    def atualizar_lista_usuarios(self):
        # pega o layout com a lista de usuarios
        lista = self.children[1].children[0]

        # Limpa a lista
        lista.clear_widgets()

        # Re-adiciona novamente todos os usuários
        app = App.get_running_app()
        for usuario in app.usuarios:
            lista.add_widget(self.criar_linha_usuario(usuario))

        # Ajustar a altura do layout com base no número de usuários
        lista.height = len(app.usuarios) * 100

    # atualiza o tamanho do background color conforme a tela
    def update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    # Componente para cada usuario criado
    def criar_linha_usuario(self, usuario):
        linha = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        linha.add_widget(Label(text=f"usuario: {usuario.nome} ({usuario.__class__.__name__})", color=(0, 0, 0, 1)))

        visualizar_btn = Button(text="Visualizar", size_hint_x = 0.20)
        visualizar_btn.bind(on_release=lambda _: self.visualizar_usuario(usuario))

        editar_btn = Button(text="Editar", size_hint_x = 0.20)
        editar_btn.bind(on_release=lambda _: self.editar_usuario(usuario))

        excluir_btn = Button(text="Excluir", size_hint_x = 0.20, on_release=lambda _: self.excluir_usuario(usuario))


        linha.add_widget(visualizar_btn)
        linha.add_widget(editar_btn)
        linha.add_widget(excluir_btn)

        return linha

    def adicionar_usuario(self, instance):
        # Abre a tela de cadastro de Usuário
        self.popup = Popup(title="Adicionar Usuário", size_hint=(0.8, 0.8))
        self.popup.content = TelaUsuario(self.popup, mode="add")
        self.popup.open()

    def visualizar_usuario(self, usuario):
        # Abre uma popup para visualizar o Usuário
        self.popup = Popup(title="Visualizar Usuário", size_hint=(0.8, 0.8))
        self.popup.content = TelaUsuario(self.popup, mode="view", usuario=usuario)
        self.popup.open()

    def editar_usuario(self, usuario):
        # Abre uma popup para editar o Usuário
        self.popup = Popup(title="Editar Usuário", size_hint=(0.8, 0.8))
        self.popup.content = TelaUsuario(self.popup, mode="edit", usuario=usuario)
        self.popup.open()

    def buscar_usuarios(self):
        # se um id for passado, retorna o correspondente
        # se não, retorna todos
        if id:
            for usuarios in self.usuarios:
                if self.id == id:
                    return self
            return None
        else:
            return self.usuarios

    # metodo para impedir exclusão de usuario associado a contrato
    def contrato_associado(self, usuario_id):
        return usuario_id not in self.contratos.values()

    def excluir_usuario(self, usuario):
        # Lógica para excluir o Usuário
        app = App.get_running_app()
        if isinstance(usuario, Administrador):
            if not usuario.is_root:
                app.usuarios.remove(usuario)  # Remove da lista de imóveis
        else:
            app.usuarios.remove(usuario)

        lista = self.children[1].children[0]
        lista.clear_widgets()
        for usuario in app.usuarios:
            lista.add_widget(self.criar_linha_usuario(usuario))

        lista.height = len(app.usuarios) * 100

class TelaUsuario(BoxLayout):
    def __init__(self, popup, mode, usuario = None, permissao = 'Locatario', **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.popup = popup
        self.mode = mode
        self.permissao = permissao
        self.usuario = usuario
        self.celular_input = None
        self.especialidade_input = None
        self.empresa_input = None

        if mode == "add":
            self.titulo = "Adicionar Usuário"
            self.permissao_input = Spinner(text = self.permissao, values= ['Administrador', 'Assistente', 'Locatario', 'PrestadorServico'])
            self.permissao_input.bind(text= self.atualiza_pagina)
            self.nome_input = TextInput(hint_text="Nome")
            self.email_input = TextInput(hint_text="Email")
            self.senha_input = TextInput(hint_text="Senha")
            self.data_nascimento_input = TextInput(hint_text="Data de Nascimento")
            self.celular_input = TextInput(hint_text="Celular")
            self.especialidade_input = TextInput(hint_text="Especialidade")
            self.empresa_input = TextInput(hint_text="Empresa")
            
        elif mode == "view" or mode == "edit":
            self.id_usuario = usuario.id
            self.titulo = "Visualizar Usuário" if mode == "view" else "Editar Usuário"
            self.permissao_input = TextInput(text=usuario.__class__.__name__, readonly=True, disabled = True)
            self.nome_input = TextInput(text=str(usuario.nome), readonly=(mode == "view"), disabled=(mode == "view"))
            self.data_nascimento_input = TextInput(text=usuario.data_nascimento, readonly=(mode == "view"), disabled=(mode == "view"))
            self.email_input = TextInput(text=usuario.email, readonly=True, disabled=True)
            self.senha_input = TextInput(text=usuario.senha, readonly=True, disabled=True)

        # Campos para código e endereço
        self.montar_tela(None)

    def montar_tela(self, instance):
        if self.mode == "view" or self.mode == "edit":
            if self.permissao_input.text == "Locatario":
                self.celular_input = TextInput(text=self.usuario.celular, readonly=(self.mode == "view"), disabled=(self.mode == "view"))
            elif self.permissao_input.text == "PrestadorServico":
                self.especialidade_input = TextInput(text=self.usuario.especialidade, readonly=(self.mode == "view"), disabled=(self.mode == "view"))
                self.empresa_input = TextInput(text=self.usuario.empresa, readonly=(self.mode == "view"), disabled=(self.mode == "view"))

        self.add_widget(Label(text="Permissão"))
        self.add_widget(self.permissao_input)
        self.add_widget(Label(text="Nome"))
        self.add_widget(self.nome_input)
        self.add_widget(Label(text="Email"))
        self.add_widget(self.email_input)
        self.add_widget(Label(text="Senha"))
        self.add_widget(self.senha_input)
        self.add_widget(Label(text="Data de Nascimento"))
        self.add_widget(self.data_nascimento_input)
        if self.permissao_input.text == "Locatario":
            self.add_widget(Label(text="Celular"))
            self.add_widget(self.celular_input)
        elif self.permissao_input.text == "PrestadorServico":
            self.add_widget(Label(text="Especialidade"))
            self.add_widget(self.especialidade_input)
            self.add_widget(Label(text="Empresa"))
            self.add_widget(self.empresa_input)
        
        # Botão de finalizar
        if self.mode == "add" or self.mode == "edit":
            finalizar_btn = Button(text="Finalizar", on_release=self.finalizar)
            self.add_widget(finalizar_btn)

        # Botão para voltar
        voltar_btn = Button(text="Voltar", on_release=self.popup.dismiss)
        self.add_widget(voltar_btn)

    def atualiza_pagina(self, instance, args):
        self.clear_widgets()
        self.montar_tela(self)


    def finalizar(self, instance):
        app = App.get_running_app()
        if self.mode == "add":
            if self.permissao_input.text == "Administrador":
                novo_usuario = Administrador(
                    nome = self.nome_input.text,
                    email = self.email_input.text,
                    senha = self.senha_input.text,
                    data_nascimento = self.data_nascimento_input.text
                )
            elif self.permissao_input.text == "Assistente":
                novo_usuario = Assistente(
                    nome = self.nome_input.text,
                    email = self.email_input.text,
                    senha = self.senha_input.text,
                    data_nascimento = self.data_nascimento_input.text
                )
            elif self.permissao_input.text == "Locatario":
                novo_usuario = Locatario(
                    nome = self.nome_input.text,
                    email = self.email_input.text,
                    senha = self.senha_input.text,
                    data_nascimento = self.data_nascimento_input.text,
                    celular = self.celular_input.text
                )
            elif self.permissao_input.text == "PrestadorServico":
                novo_usuario = PrestadorServico(
                    nome = self.nome_input.text,
                    email = self.email_input.text,
                    senha = self.senha_input.text,
                    data_nascimento = self.data_nascimento_input.text,
                    especialidade = self.especialidade_input.text,
                    empresa = self.empresa_input.text
                )
                print(novo_usuario.especialidade)
            app.usuarios.append(novo_usuario)

        elif self.mode == "edit":
            for usuario in app.usuarios:
                if usuario.id == self.id_usuario:
                    usuario.nome = self.nome_input.text
                    usuario.data_nascimento = self.data_nascimento_input.text
                    if isinstance(usuario, Locatario):
                        usuario.celular = self.celular_input.text
                    elif isinstance(usuario, PrestadorServico):
                        usuario.especialidade = self.especialidade_input
                        usuario.empresa = self.empresa_input
    
        tela_inicial = app.root
        tela_inicial.atualizar_lista_usuarios()

        self.popup.dismiss()

class selfApp(App):
    def build(self):
        self.usuarios = [  # valores de teste
            Administrador(nome="Root", email = "root@root", senha = "root", data_nascimento = "01/01/1990", is_root=True),
            Locatario(nome="Maria", email = "maria@gmail.com", senha = "123456", data_nascimento = "01/01/1992"),
            Locatario(nome="Joao", email = "joao@gmail.com", senha = "123456", data_nascimento = "01/01/1990"),
            ]

        tela_inicial = TelaInicial(usuarios=self.usuarios)
        return tela_inicial


if __name__ == '__main__':
    selfApp().run()
