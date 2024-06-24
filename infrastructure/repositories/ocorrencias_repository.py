from uuid import UUID

from sqlalchemy.orm import joinedload

from domain.models.ocorrencia import Ocorrencia
from infrastructure.configs.connection import Connection
from infrastructure.mappers.OcorrenciaInput import OcorrenciaInputMapper
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
    def get_all_to_domain(self):
        with Connection() as connection:
            ocorrencias_from_db = connection.session.query(Ocorrencias).options(joinedload(Ocorrencias.imagens)).all()
            ocorrencias_domain = []
            for ocorrencia_db in ocorrencias_from_db:
                ocorrencia_domain = OcorrenciaInputMapper.map_ocorrencia_to_domain(ocorrencia_db)
                ocorrencias_domain.append(ocorrencia_domain)
            return ocorrencias_domain

    def get_all(self):
        with Connection() as connection:
            result = connection.session.query(Ocorrencias).options(joinedload(Ocorrencias.imagens)).all()
            return result

    def is_session_attached(self, ocorrencia: Ocorrencias) -> bool:
        """
        Verifica se a ocorrência está associada a uma sessão ativa do SQLAlchemy.
        """
        with Connection() as connection:
            return connection.session.object_session(ocorrencia) is not None

