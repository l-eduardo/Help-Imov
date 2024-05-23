from uuid import UUID
from infrastructure.configs.connection import Connection
from infrastructure.models.vistorias import Vistorias


class VistoriasRepositories:
    def get_all(self) -> list[Vistorias]:
        with Connection() as connection:
            return connection.session.query(Vistorias).all()

    def get_by_id(self, id: UUID) -> Vistorias:
        with Connection() as connection:
            return connection.session.query(Vistorias) \
                .filter(Vistorias.id == id) \
                .first()

    def insert(self, vistoria: Vistorias) -> Vistorias:
        with Connection() as connection:
            connection.session.add(vistoria)
            connection.session.commit()
            return vistoria

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            connection.session.query(Vistorias).filter(Vistorias.id == id).delete()


