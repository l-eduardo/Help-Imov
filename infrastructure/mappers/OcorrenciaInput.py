from domain.models.ocorrencia import Ocorrencia
from infrastructure.mappers.ChatInput import ChatInputMapper
from infrastructure.models.ocorrencias import Ocorrencias  # Importe o modelo de infraestrutura


class OcorrenciaInputMapper:

    @staticmethod
    def map_ocorrencia_to_domain(ocorrencia_db: Ocorrencias) -> Ocorrencia:
        # Aqui você faz o mapeamento dos atributos
        return Ocorrencia(
            id=ocorrencia_db.id,
            titulo=ocorrencia_db.titulo,
            descricao=ocorrencia_db.descricao,
            criador_id=ocorrencia_db.criador_id,
            prestador_id=ocorrencia_db.prestador_id,
            status=ocorrencia_db.status,  # Supondo que o status seja mapeado corretamente
            imagens=ocorrencia_db.imagens,
            chat=ChatInputMapper.map_chat(ocorrencia_db.chat),
            data_criacao=ocorrencia_db.data_criacao,
        )
