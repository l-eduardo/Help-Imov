from infrastructure.configs.connection import Connection
from infrastructure.models.usuarios_identity_infos import UsuariosIdentityInfos

class AuthInfosRepository:
    def autenticar(self, email, senha):
        with Connection() as connection:
            return connection.session.query(UsuariosIdentityInfos)\
                .filter(UsuariosIdentityInfos.email == email, UsuariosIdentityInfos.senha == senha)\
                .first() != None
