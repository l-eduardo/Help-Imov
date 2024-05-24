import functools

from domain.exceptions.UserWithNoInfosException import UserWithNoInfosException
from domain.models.session import Session
from infrastructure.repositories.administradores_repository import AdministradoresRepository
from infrastructure.repositories.user_identity_repository import UserIdentityRepository


class SessionController:
    session : Session | None = None
    def __init__(self):
        self.__session_repository = UserIdentityRepository()
        pass

    def get_new_session(self, id) -> None:
        user_identity_infos = self.__session_repository.get_user_identity_by_id(id)

        role = self.__session_repository.check_user_table(id)

        if role == None:
            raise UserWithNoInfosException()

        is_root = False
        is_admin = False

        if role == "Administrador":
            is_admin = True
            is_root = AdministradoresRepository().is_root(id)

        SessionController.session = Session(id, user_identity_infos.email, role, is_root, is_admin, True)

    def autheticate(self, email, password):
        return self.__session_repository.get_user_identity_by_login_infos(email, password)

    def inject_session_data(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            kwargs['session'] = SessionController.session

            result = func(*args, **kwargs)

            return result

        return wrapper
