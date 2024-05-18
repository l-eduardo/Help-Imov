from uuid import UUID
from application.interfaces.UserRepository import UserRepository
from infrastructure.configs.connection import Connection
from infrastructure.models.usuarios_identity_infos import UsuariosIdentityInfos

class UserIdentityRepository(UserRepository):
    def autenticar(self, email, senha) -> bool:
        with Connection() as connection:
            return connection.session.query(UsuariosIdentityInfos)\
                .filter(UsuariosIdentityInfos.email == email, UsuariosIdentityInfos.senha == senha)\
                .first() != None

    def get_user(self, user_id: UUID):
        raise NotImplementedError

    def get_user_by_login_infos(self, email: str, senha: str):
        with Connection() as connection:
            return connection.session.query(UsuariosIdentityInfos)\
                .filter(UsuariosIdentityInfos.email == email, UsuariosIdentityInfos.senha == senha)\
                .first()

    def save_user(self, user):
        raise NotImplementedError

    def delete_user(self, user_id: UUID):
        raise NotImplementedError

    def get_all_users(self):
        raise NotImplementedError

