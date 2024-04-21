from uuid import UUID
from infrastructure.configs.connection import Connection
from infrastructure.models.administradores import Administradores
from infrastructure.models.usuarios_identity_infos import UsuariosIdentityInfos

class AdministradorRepository:
    def get_by_id(self, id: UUID):
        with Connection() as connection:
            result = connection.session.query(Administradores)\
            .filter(Administradores.id == id)\
            .first()

            if result is None:
                return None

            return result

