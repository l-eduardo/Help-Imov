from uuid import UUID
from infrastructure.configs.connection import Connection
from infrastructure.models.assistentes import Assistentes


class AssistentesRepository:
    def get_all(self) -> list[Assistentes]:
        with Connection() as connection:
            return connection.session.query(Assistentes).all()

    def get_by_id(self, id: UUID) -> Assistentes:
        with Connection() as connection:
            return connection.session.query(Assistentes)\
                .filter(Assistentes.id == id)\
                .first()

    def insert(self, assist) -> Assistentes:
        with Connection() as connection:
            connection.session.add(assist)
            return assist

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            connection.session.query(Assistentes).filter(Assistentes.id == id).delete()
