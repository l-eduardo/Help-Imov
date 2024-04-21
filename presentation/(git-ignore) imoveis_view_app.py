from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from typing import List
from kivy.uix.widget import Widget
from domain.models import imovel
import uuid


class Imovel:
    def __init__(self, codigo: int, endereco: str, imagens: List[List[bytes]], id: uuid.UUID = uuid.UUID(int=0)):
        self.id = id if id != uuid.UUID(int=0) else uuid.uuid4()
        self.codigo = codigo
        self.endereco = endereco
        self.imagens = imagens


class TelaInicial(BoxLayout):
    def __init__(self, imoveis, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Cor de fundo (cinza claro)
            self.bg = Rectangle(size=self.size, pos=self.pos)

        # Atualizar o tamanho do retângulo ao redimensionar
        self.bind(size=self.update_bg, pos=self.update_bg)

        # Layout do topo da tela
        topo = BoxLayout(size_hint=(1, 0.1))

        logo = Image(source='assets/help-imov-logo.png')

        titulo = Label(text='Imóveis',
                       height='48dp',
                       halign='center',
                       valign='middle',
                       color=(0, 0, 0, 1),
                       font_size='24sp')

        adicionar_btn = Button(text='Adicionar')

        spacer = Widget(size_hint_x=2)
        spacer_2 = Widget(size_hint_x=2)
        spacer_3 = Widget(size_hint=(1, 0.6))

        adicionar_btn.bind(on_release=self.adicionar_imovel)

        topo.add_widget(logo)
        topo.add_widget(spacer_2)
        topo.add_widget(titulo)
        topo.add_widget(spacer)
        topo.add_widget(adicionar_btn)

        self.add_widget(topo)
        self.add_widget(spacer_3)

        scroll_view = ScrollView(size_hint=(1, 0.8))
        lista = BoxLayout(orientation='vertical', size_hint_y=None)
        lista.bind(minimum_height=scroll_view.setter('height'))

        # Lista de imóveis cadastrados
        for imovel in imoveis:
            lista.add_widget(self.criar_linha_imovel(imovel))

        scroll_view.add_widget(lista)
        self.add_widget(scroll_view)

        # Botão para voltar
        voltar_btn = Button(text="Voltar", size_hint=(1, 0.1))
        self.add_widget(voltar_btn)

    # renderiza a lista para cada novo imovel criado
    def atualizar_lista_imoveis(self):
        # pega o layout com a lista de imoveis
        lista = self.children[1].children[0]

        # Limpa a lista
        lista.clear_widgets()

        # Re-adiciona novamente todos os imóveis
        app = App.get_running_app()
        for imovel in app.imoveis:
            lista.add_widget(self.criar_linha_imovel(imovel))

        # Ajustar a altura do layout com base no número de imóveis
        lista.height = len(app.imoveis) * 100

    # atualiza o tamanho do background color conforme a tela
    def update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    # Componente para cada imovel criado
    def criar_linha_imovel(self, imovel):
        linha = BoxLayout(orientation='horizontal',
                          size_hint=(1, 0.1),
                          )

        linha.add_widget(Label(text=f"Imovel: {imovel.codigo}",
                               color=(0, 0, 0, 1)))

        visualizar_btn = Button(text="Visualizar")
        visualizar_btn.bind(on_release=lambda _: self.visualizar_imovel(imovel))

        editar_btn = Button(text="Editar")
        editar_btn.bind(on_release=lambda _: self.editar_imovel(imovel))

        excluir_btn = Button(text="Excluir")
        excluir_btn.bind(on_release=lambda _: self.excluir_imovel(imovel))

        linha.add_widget(visualizar_btn)
        linha.add_widget(editar_btn)
        linha.add_widget(excluir_btn)

        return linha

    def adicionar_imovel(self, instance):
        # Abre a tela de cadastro de imóvel
        self.popup = Popup(title="Adicionar Imóvel", size_hint=(0.8, 0.8))
        self.popup.content = TelaImovel(self.popup, mode="add")
        self.popup.open()

    def visualizar_imovel(self, imovel):
        # Abre uma popup para visualizar o imóvel
        self.popup = Popup(title="Visualizar Imóvel", size_hint=(0.8, 0.8))
        self.popup.content = TelaImovel(self.popup, mode="view", imovel=imovel)
        self.popup.open()

    def editar_imovel(self, imovel):
        # Abre uma popup para editar o imóvel
        self.popup = Popup(title="Editar Imóvel", size_hint=(0.8, 0.8))
        self.popup.content = TelaImovel(self.popup, mode="edit", imovel=imovel)
        self.popup.open()

    def buscar_imoveis(self):
        # se um id for passado, retorna o correspondente
        # se não, retorna todos
        if id:
            for imoveis in self.imoveis:
                if imovel.id == id:
                    return imovel
            return None
        else:
            return self.imoveis

    # metodo para impedir exclusão de imovel associado a contrato
    def contrato_associado(self, imovel_id):
        return imovel_id not in self.contratos.values()

    def excluir_imovel(self, imovel):
        # Lógica para excluir o imóvel
        app = App.get_running_app()
        app.imoveis.remove(imovel)  # Remove da lista de imóveis

        lista = self.children[1].children[0]
        lista.clear_widgets()
        for imovel in app.imoveis:
            lista.add_widget(self.criar_linha_imovel(imovel))

        lista.height = len(app.imoveis) * 100


class TelaImovel(BoxLayout):
    def __init__(self, popup, mode, imovel=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.popup = popup
        self.mode = mode

        if mode == "add":
            self.titulo = "Adicionar Imóvel"
            self.codigo_input = TextInput(hint_text="Código")
            self.endereco_input = TextInput(hint_text="Endereço")
            self.imagens = []
        elif mode == "view" or mode == "edit":
            self.titulo = "Visualizar Imóvel" if mode == "view" else "Editar Imóvel"
            self.codigo_input = TextInput(text=str(imovel.codigo), readonly=(mode == "view"))
            self.endereco_input = TextInput(text=imovel.endereco, readonly=(mode == "view"))

            self.imagens = imovel.imagens if imovel else []
            for img_path in self.imagens:
                imagem_widget = Image(source=img_path)
                self.add_widget(imagem_widget)

        # Campos para código e endereço
        self.add_widget(Label(text="Código"))
        self.add_widget(self.codigo_input)
        self.add_widget(Label(text="Endereço"))
        self.add_widget(self.endereco_input)

        # Campo para adição de imagens
        self.filechooser = FileChooserIconView(filters=['*.png'])
        self.filechooser.size_hint_y = 3
        self.filechooser.bind(on_selection=self.carregar_imagem)
        self.add_widget(self.filechooser)

        # Botão de finalizar
        if mode != "view":
            finalizar_btn = Button(text="Finalizar")
            finalizar_btn.bind(on_release=self.finalizar)
            self.add_widget(finalizar_btn)

        # Botão para voltar
        voltar_btn = Button(text="Voltar")
        voltar_btn.bind(on_release=self.popup.dismiss)
        self.add_widget(voltar_btn)

    def carregar_imagem(self, filechooser, selection):
        if selection:
            image_path = selection[0]
            print("Imagem selecionada:", image_path)
            self.imagens.append(image_path)

            imagem = Image(source=image_path)
            self.add_widget(imagem)

    def finalizar(self, instance):
        if self.mode == "add":
            app = App.get_running_app()
            novo_imovel = Imovel(
                codigo=int(self.codigo_input.text),
                endereco=self.endereco_input.text,
                imagens=self.imagens,
            )
            app.imoveis.append(novo_imovel)

            tela_inicial = app.root
            tela_inicial.atualizar_lista_imoveis()

        elif self.mode == "edit":
            imovel.codigo = int(self.codigo_input.text)
            imovel.endereco = self.endereco_input.text
            imovel.imagens = self.imagens

        self.popup.dismiss()


