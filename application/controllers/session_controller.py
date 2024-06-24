import functools
import uuid

from domain.exceptions.UserWithNoInfosException import UserWithNoInfosException
from domain.models.session import Session
from infrastructure.repositories.administradores_repository import AdministradoresRepository
from infrastructure.repositories.user_identity_repository import UserIdentityRepository


class SessionController:
    session: Session | None = None
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

        SessionController.session = Session(user_id=id,
                                    user_email=user_identity_infos.email,
                                    user_role=role,
                                    is_root=is_root,
                                    is_admin=is_admin,
                                    is_valid=True,
                                    session_id=uuid.uuid4())

    def autheticate(self, email, password):
        return self.__session_repository.get_user_identity_by_login_infos(email, password)

    def get_current_user(self):
        return SessionController.session

    def inject_session_data(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            kwargs['session'] = SessionController.session

            result = func(*args, **kwargs)

            return result

        return wrapper
