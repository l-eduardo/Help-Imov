from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from dotenv import load_dotenv

from infrastructure.repositories.imoveis_repository import ImoveisRepository
from presentation.contrato_view import ContratoScreen, ListaContratosScreen
from presentation.views.imoveis_list_view import ListImoveisView
from presentation.views.login_view import LoginView

load_dotenv()

class LoginApp(App):
    def build(self):
        screen_manager = ScreenManager()
        login_screen = LoginView(name='login')
        main_screen = ListImoveisView(name='imoveis', imoveis_repository=ImoveisRepository())

        screen_manager.add_widget(login_screen)
        screen_manager.add_widget(main_screen)
        screen_manager.add_widget(ListaContratosScreen(name='listacontratos'))
        screen_manager.add_widget(ContratoScreen(name='contrato'))

        return screen_manager

LoginApp().run()
