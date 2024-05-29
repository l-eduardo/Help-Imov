from uuid import UUID
from infrastructure.configs.connection import Connection
from infrastructure.models.administradores import Administradores
from infrastructure.models.usuarios_identity_infos import UsuariosIdentityInfos

class AdministradoresRepository:
    def get_by_id(self, id: UUID):
        with Connection() as connection:
            result = connection.session.query(Administradores)\
            .filter(Administradores.id == id)\
            .first()

            if result is None:
                return None

            return result

    def insert(self, administrador: Administradores) -> Administradores:
        with Connection() as connection:
            connection.session.add(administrador)
            return administrador

    def is_root(self, id: UUID):
        with Connection() as connection:
            result = connection.session.query(Administradores)\
            .filter(Administradores.id == id)\
            .filter(Administradores.e_root == True)\
            .first()

            if result is None:
                return False

            return result.e_root
