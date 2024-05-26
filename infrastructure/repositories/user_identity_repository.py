from uuid import UUID
from application.interfaces.UserRepository import UserRepository
from infrastructure.configs.connection import Connection
from infrastructure.models.usuarios_identity_infos import UsuariosIdentityInfos
from infrastructure.repositories.sql.pure_sql_queries import PureSqlQueries

class UserIdentityRepository(UserRepository):
    def authenticate(self, email, senha) -> bool:
        with Connection() as connection:
            return connection.session.query(UsuariosIdentityInfos)\
                .filter(UsuariosIdentityInfos.email == email, UsuariosIdentityInfos.senha == senha)\
                .first() != None

    def get_user(self, user_id: UUID):
        raise NotImplementedError

    def check_user_table(self, id: UUID):
        with Connection() as connection:
            query_result = connection.session.execute(PureSqlQueries.check_id_in_tables(id)).first()

            if query_result == None:
                return None

            return query_result[0]

    def get_user_identity_by_login_infos(self, email: str, senha: str):
        with Connection() as connection:
            user_login_infos = connection.session.query(UsuariosIdentityInfos)\
                .filter(UsuariosIdentityInfos.email == email, UsuariosIdentityInfos.senha == senha)\
                .first()

            return user_login_infos

    def get_user_identity_by_id(self, user_id: UUID):
        with Connection() as connection:
            user_identity = connection.session.query(UsuariosIdentityInfos)\
                .filter(UsuariosIdentityInfos.id == user_id)\
                .first()

            return user_identity

    def save_user(self, user):
        raise NotImplementedError

    def delete_user(self, user_id: UUID):
        raise NotImplementedError

    def get_all_users(self):
        raise NotImplementedError
