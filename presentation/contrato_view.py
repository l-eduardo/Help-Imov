from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

# Definição das telas
class ContratoScreen(Screen):

    def retorna_contrato(self):
        self.reset_screen()
        return {
            "dataInicio": self.ids.data_inicio_input.text,
            "dataFim": self.ids.data_fim_input.text,
            "locatario": self.ids.locatario_spinner.text,  # obter texto no Spinner de locatário
            "imovel": self.ids.imovel_spinner.text  # obter texto selecionado no Spinner de imóvel
        }

    def reset_screen(self):
        # Resetando os Spinners para o primeiro valor ou um valor padrão
        self.ids.locatario_spinner.text = 'Selecione o locatário...'
        self.ids.imovel_spinner.text = 'Selecione o imóvel...'

        # Resetando os TextInput para vazio
        for child in self.walk():
            if isinstance(child, TextInput):
                child.text = ''

class ListaContratosScreen(Screen):
    def update_contratos_view(self, contratos):
        self.ids.contratos_list.clear_widgets()  # Limpa a lista atual
        for contrato in contratos:
            # Aqui você pode criar uma representação visual para cada contrato
            label = Label(text=f"Contrato de {contrato.locatario} para {contrato.imovel}")
            self.ids.contratos_list.add_widget(label)

    def update_active_status(self, contrato_id, is_active):
        # Aqui você pode adicionar lógica para atualizar o status no banco de dados ou outro armazenamento
        print(f"Status do {contrato_id} alterado para {'ativo' if is_active else 'inativo'}")


class EditarContratoScreen(Screen):
    def load_contrato(self, locatario, imovel):
        self.ids.locatario_spinner.text = locatario
        self.ids.imovel_spinner.text = imovel

# Gerenciador de telas
class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(ListaContratosScreen(name='listacontratos'))
        self.add_widget(ContratoScreen(name='contrato'))

# Carregando os arquivos .kv
Builder.load_file('contrato.kv')
Builder.load_file('listacontratos.kv')

# Aplicativo principal
class MainApp(App):
    def build(self):
        return MyScreenManager()

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    MainApp().run()
