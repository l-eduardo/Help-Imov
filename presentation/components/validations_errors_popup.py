import PySimpleGUI as sg


class ValidationErrorsPopup:
    @staticmethod
    def show_errors(errors):

        error_strings = '\n\n'.join(errors)
        sg.popup_timed(error_strings, title="Erros de validacao de Ocorrencia")
