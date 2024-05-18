import functools

from infrastructure.repositories.user_identity_repository import UserIdentityRepository


class SessionController:
    def __init__(self):
        self.__session = {}
        self.__session_repository = UserIdentityRepository()
        pass

    def get_new_session(self, id):
        return self.__session

    def autheticate(self, email, password):
        return self.__session_repository.get_user_by_login_infos(email, password)

    def method_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Code to be executed before calling the original method
            print("Executing code before the method call")

            # Call the original method
            result = func(*args, **kwargs)

            # Code to be executed after calling the original method
            print("Executing code after the method call")

            # Return the result
            return result

        return wrapper
