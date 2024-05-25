from uuid import UUID
from domain.models.ocorrencia import Ocorrencia
from infrastructure.configs.connection import Connection
from infrastructure.mappers.OcorrenciaOutput import OcorrenciaOutputMapper
from infrastructure.models.ocorrencias import Ocorrencias


class OcorrenciasRepository:
    def insert(self, ocorrencia: Ocorrencia, contrato_id: UUID) -> Ocorrencia:
        ocorrencia_to_db = OcorrenciaOutputMapper.map_ocorrencia(ocorrencia_from_domain=ocorrencia, contrato_id=contrato_id)

        with Connection() as connection:

            connection.session.add(ocorrencia_to_db)
            connection.session.commit()
            return ocorrencia

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            connection.session.query(Ocorrencias).filter(Ocorrencias.id == id).delete()
