from kivy.app import App
from dotenv import load_dotenv

from presentation.views.login.loginView import LoginWindow

load_dotenv()

class LoginApp(App):
    def build(self):
        return LoginWindow()

LoginApp().run()
