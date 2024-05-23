from uuid import UUID
from infrastructure.configs.connection import Connection
from infrastructure.models.ocorrencias import Ocorrencias


class OcorrenciasRepository:
    def get_all(self) -> list[Ocorrencias]:
        with Connection() as connection:
            return connection.session.query(Ocorrencias).all()

    def get_by_id(self, id: UUID) -> Ocorrencias:
        with Connection() as connection:
            return connection.session.query(Ocorrencias)\
                .filter(Ocorrencias.id == id)\
                .first()

    def insert(self, assist) -> Ocorrencias:
        with Connection() as connection:
            connection.session.add(assist)
            return assist

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            connection.session.query(Ocorrencias).filter(Ocorrencias.id == id).delete()
