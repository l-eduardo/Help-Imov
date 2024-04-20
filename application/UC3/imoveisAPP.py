from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.image import Image
from typing import List
import uuid


class Imovel:
    def __init__(self, codigo: int, endereco: str, imagens: List[List[bytes]], id: uuid.UUID = uuid.UUID(int=0)):
        self.id = id if id != uuid.UUID(int=0) else uuid.uuid4()
        self.codigo = codigo
        self.endereco = endereco
        self.imagens = imagens

