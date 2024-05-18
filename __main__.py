from dotenv import load_dotenv

from application.controllers.main_controller import MainController


if __name__ == '__main__':
    load_dotenv()
    MainController().run()
