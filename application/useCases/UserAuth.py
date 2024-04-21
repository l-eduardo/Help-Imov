class UserAuth:
    def __init__(self, AuthInfosRepository):
        self.AuthInfosRepository = AuthInfosRepository


    def login(self, email, password):
        if self.AuthInfosRepository.autenticar(email, password):

            return

