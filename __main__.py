from dotenv import load_dotenv

from application.controllers.main_controller import MainController
from infrastructure.repositories.assistentes_repository import AssistentesRepository
from infrastructure.repositories.user_identity_repository import UserIdentityRepository


if __name__ == '__main__':
    load_dotenv()
    MainController().run()
