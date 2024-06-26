from abc import ABC, abstractmethod
import uuid


class UserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: uuid.UUID):
        pass

    @abstractmethod
    def get_user_identity_by_login_infos(self, email: str, senha: str):
        pass

    @abstractmethod
    def save_user(self, user):
        pass

    @abstractmethod
    def delete_user(self, user_id: uuid.UUID):
        pass
