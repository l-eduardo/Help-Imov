from uuid import UUID

from domain.models.ocorrencia import Ocorrencia
from infrastructure.models.ocorrencias import Ocorrencias


class OcorrenciaOutputMapper:
    @staticmethod
    def map_ocorrencia(ocorrencia_from_domain: 'Ocorrencia', contrato_id: UUID) -> 'Ocorrencias':

        ocorrencia_to_db = Ocorrencias()
        ocorrencia_to_db.id = ocorrencia_from_domain.id
        ocorrencia_to_db.titulo = ocorrencia_from_domain.titulo
        ocorrencia_to_db.descricao = ocorrencia_from_domain.descricao
        ocorrencia_to_db.status = ocorrencia_from_domain.status.name
        ocorrencia_to_db.data_criacao = ocorrencia_from_domain.data_criacao
        ocorrencia_to_db.contrato_id = contrato_id

        return ocorrencia_to_db
