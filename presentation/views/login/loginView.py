from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from dotenv import load_dotenv

from application.useCases.UserAuth import UserAuth
from infrastructure.repositories.auth_infos_repository import AuthInfosRepository

class LoginWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginWindow, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [100, 50, 100, 50]

        self.add_widget(Label(text='Email'))
        self.username_input = TextInput(multiline=False)
        self.add_widget(self.username_input)

        self.add_widget(Label(text='Password'))
        self.password_input = TextInput(multiline=False, password=True)
        self.add_widget(self.password_input)

        self.login_button = Button(text='Login', on_release=self.login)
        self.add_widget(self.login_button)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        # Add your login logic here

        print(f'Username: {username}, Password: {password}')
        UserAuth(AuthInfosRepository=AuthInfosRepository()).login(username, password)
        self.username_input.text = ''
        self.password_input.text = ''

class LoginApp(App):
    def build(self):
        return LoginWindow()

if __name__ == '__main__':
    LoginApp().run()
