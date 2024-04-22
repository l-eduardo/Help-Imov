from uuid import UUID
from infrastructure.configs.connection import Connection
from infrastructure.models.solicitacoes import Solicitacoes


class SolicitacoesRepository:
    def get_all(self) -> list[Solicitacoes]:
        with Connection() as connection:
            return connection.session.query(Solicitacoes).all()

    def get_by_id(self, id: UUID) -> Solicitacoes:
        with Connection() as connection:
            return connection.session.query(Solicitacoes)\
                .filter(Solicitacoes.id == id)\
                .first()

    def insert(self, assist) -> Solicitacoes:
        with Connection() as connection:
            connection.session.add(assist)
            return assist

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            connection.session.query(Solicitacoes).filter(Solicitacoes.id == id).delete()
