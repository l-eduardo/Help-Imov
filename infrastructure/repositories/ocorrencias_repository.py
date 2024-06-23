from uuid import UUID
from domain.models.ocorrencia import Ocorrencia
from infrastructure.configs.connection import Connection
from infrastructure.mappers.OcorrenciaOutput import OcorrenciaOutputMapper
from infrastructure.models.ocorrencias import Ocorrencias
from infrastructure.repositories.prestadores_servicos_repository import PrestadoresServicosRepository


class OcorrenciasRepository:

    def insert(self, ocorrencia: Ocorrencia, contrato_id: UUID) -> Ocorrencia:
        ocorrencia_to_db = OcorrenciaOutputMapper.map_ocorrencia(ocorrencia_from_domain=ocorrencia, contrato_id=contrato_id)

        with Connection() as connection:

            connection.session.add(ocorrencia_to_db)
            connection.session.commit()
            return ocorrencia

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            result = connection.session.query(Ocorrencias).filter(Ocorrencias.id == str(id)).delete()
            connection.session.commit()

    def update(self, ocorrencia: Ocorrencia) -> Ocorrencia:
        prestadores_servicos_repository = PrestadoresServicosRepository()
        prestador_id = prestadores_servicos_repository.get_id_by_name(str(ocorrencia.prestador_id))

        with Connection() as connection:
            result = connection.session.query(Ocorrencias).filter(Ocorrencias.id == str(ocorrencia.id)).update(
                {
                    "titulo": ocorrencia.titulo,
                    "descricao": ocorrencia.descricao,
                    "prestador_id": ocorrencia.prestador_id,
                    "status": ocorrencia.status.name
                }
            )
            connection.session.commit()
            return ocorrencia
    
    def get_by_id(self, id_ocorrencia):
        with Connection() as connection:
            result = connection.session.query(Ocorrencias).filter(Ocorrencias.id == str(id_ocorrencia)).first()
            return result

rep = OcorrenciasRepository()
rep.get_by_id(UUID('0b72d84e-2b01-4448-8ca1-31e1ced8a00d'))

