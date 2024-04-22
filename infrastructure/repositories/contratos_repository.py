from uuid import UUID
from infrastructure.configs.connection import Connection
from infrastructure.models.contratos import Contratos

class ContratosRepositories:
    def get_all(self) -> list[Contratos]:
        with Connection() as connection:
            return connection.session.query(Contratos).all()

    def get_by_id(self, id: UUID) -> Contratos:
        with Connection() as connection:
            return connection.session.query(Contratos)\
                .filter(Contratos.id == id)\
                .first()

    def get_by_locatario_id(self, locatario_id: UUID) -> list[Contratos]:
        with Connection() as connection:
            return connection.session.query(Contratos)\
                .filter(Contratos.locatario_id == locatario_id)\
                .all()

    def insert(self, contrato: Contratos) -> Contratos:
        with Connection() as connection:
            connection.session.add(contrato)
            return contrato
