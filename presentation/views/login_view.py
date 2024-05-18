import PySimpleGUI as sg

from application.controllers.session_controller import SessionController


class LoginView:
    def open(self):
        window = self.__init_layout()

        event, text = window.read()

        window.close()
        return event, text

    def __init_layout(self):
        centrilizedText = sg.Text("Login")
        centrilizedButtons = [sg.Button("Ok", size=(10,1)), sg.Button("Cancel", size=(10,1))]

        layout = [  [sg.Column([[centrilizedText]], justification="center")],
                    [sg.Text("Email", expand_x=True), sg.InputText(key="email", tooltip="email", size=(30,1))],
                    [sg.Text("Senha", expand_x=True), sg.InputText(key="password" ,tooltip="teste",password_char="*", size=(30,1))],
                    [sg.Column([centrilizedButtons], justification="center")] ]


        window = sg.Window("Help Imov", layout)

        return window

    def error_popup(self, message):
        sg.popup_no_titlebar(message)

    def __auth(self, email, password):
        print(SessionController().autheticate(email, password))
