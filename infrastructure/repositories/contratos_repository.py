from uuid import UUID

from sqlalchemy.orm import joinedload

from infrastructure.configs.connection import Connection
from infrastructure.models.contratos import Contratos
from infrastructure.mappers.ContratoInput import ContratoInputMapper
from infrastructure.models.imoveis import Imoveis
from infrastructure.models.locatarios import Locatarios
from infrastructure.models.ocorrencias import Ocorrencias
from infrastructure.models.solicitacoes import Solicitacoes


from infrastructure.models.ocorrencias import Ocorrencias

class ContratosRepositories:
    def get_all(self) -> list[Contratos]:
        with Connection() as connection:
            result = connection.session.query(Contratos).all()
            result_mapped = [ContratoInputMapper.map_contrato(x) for x in result]

            return result_mapped

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
            connection.session.commit()
            return contrato


