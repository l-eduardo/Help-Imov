import uuid

from domain.models.ocorrencia import Ocorrencia
from infrastructure.mappers.ImagemOutput import ImagemOutputMapper
from infrastructure.models.imagens import Imagens
from infrastructure.models.ocorrencias import Ocorrencias


class OcorrenciaOutputMapper:
    @staticmethod
    def map_ocorrencia(ocorrencia_from_domain: 'Ocorrencia', contrato_id: uuid.UUID) -> 'Ocorrencias':
        imagens = []
        for imagem in ocorrencia_from_domain.imagens:
            imagens.append(ImagemOutputMapper.map(imagem, ocorrencia_id=ocorrencia_from_domain.id))

        ocorrencia_to_db = Ocorrencias()
        ocorrencia_to_db.id = str(ocorrencia_from_domain.id)
        ocorrencia_to_db.titulo = ocorrencia_from_domain.titulo
        ocorrencia_to_db.descricao = ocorrencia_from_domain.descricao
        ocorrencia_to_db.status = ocorrencia_from_domain.status.name
        ocorrencia_to_db.data_criacao = ocorrencia_from_domain.data_criacao
        ocorrencia_to_db.imagens = imagens
        ocorrencia_to_db.contrato_id = contrato_id
        ocorrencia_to_db.criador_id = ocorrencia_from_domain.criador_id
        ocorrencia_to_db.prestador_id = ocorrencia_from_domain.prestador_id if ocorrencia_from_domain.prestador_id else None


        return ocorrencia_to_db
