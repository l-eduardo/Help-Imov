from application.interfaces.UserRepository import UserRepository


class UserAuth:
    def __init__(self, AuthInfosRepository: UserRepository):
        self.AuthInfosRepository = AuthInfosRepository

    def login(self, email, password):
        return self.AuthInfosRepository.get_user_by_login_infos(email, password) != None
