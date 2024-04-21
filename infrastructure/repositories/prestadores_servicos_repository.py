from uuid import UUID
from infrastructure.configs.connection import Connection
from infrastructure.models.prestadores_servico import PrestadoresServicos


class PrestadoresServicosRepository:
    def get_all(self) -> list[PrestadoresServicos]:
        with Connection() as connection:
            return connection.session.query(PrestadoresServicos).all()

    def get_by_id(self, id: UUID) -> PrestadoresServicos:
        with Connection() as connection:
            return connection.session.query(PrestadoresServicos)\
                .filter(PrestadoresServicos.id == id)\
                .first()

    def insert(self, assist) -> PrestadoresServicos:
        with Connection() as connection:
            connection.session.add(assist)
            return assist

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            connection.session.query(PrestadoresServicos).filter(PrestadoresServicos.id == id).delete()
