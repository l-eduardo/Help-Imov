from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.image import Image

from domain.models import imovel
import uuid

from domain.models.imovel import Imovel


class ImovelModal(BoxLayout):
    def __init__(self, popup, mode, imovel: Imovel | None, **kwargs):
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

            # self.imagens = imovel.imagens if imovel else []
            # for img_path in self.imagens:
            #     imagem_widget = Image(source=img_path)
            #     self.add_widget(imagem_widget)

        # Campos para código e endereço
        self.add_widget(Label(text="Código"))
        self.add_widget(self.codigo_input)
        self.add_widget(Label(text="Endereço"))
        self.add_widget(self.endereco_input)

        # Campo para adição de imagens
        # self.filechooser = FileChooserIconView(filters=['*.png'])
        # self.filechooser.size_hint_y = 3
        # self.filechooser.bind(on_selection=self.carregar_imagem)
        # self.add_widget(self.filechooser)

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
        print("Imagem selecionada:", selection)
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
