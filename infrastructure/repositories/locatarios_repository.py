from uuid import UUID
from infrastructure.configs.connection import Connection
from infrastructure.models.locatarios import Locatarios
from infrastructure.mappers.UsersInput import UsersInputMapper


class LocatariosRepository:
    def get_all(self) -> list[Locatarios]:
        with Connection() as connection:
            result = connection.session.query(Locatarios).all()
            return [UsersInputMapper.map_locatario_input(x) for x in result]

    def get_by_id(self, id: UUID) -> Locatarios:
        with Connection() as connection:
            return connection.session.query(Locatarios)\
                .filter(Locatarios.id == id)\
                .first()

    def insert(self, locatario: Locatarios) -> Locatarios:
        with Connection() as connection:
            connection.session.add(locatario)
            return locatario

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            connection.session.query(Locatarios).filter(Locatarios.id == id).delete()
