class UserAuth:
    def __init__(self, AuthInfosRepository):
        self.AuthInfosRepository = AuthInfosRepository

    def login(self, email, password):
        return self.AuthInfosRepository.autenticar(email, password)
