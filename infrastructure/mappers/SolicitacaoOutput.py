from uuid import UUID

from domain.models.solicitacao import Solicitacao
from infrastructure.models.solicitacoes import Solicitacoes


class SolicitacaoOutputMapper:
    @staticmethod
    def map_solicitacao(solicitacao_from_domain: 'Solicitacao', contrato_id: UUID) -> 'Solicitacoes':

        solicitacao_to_db = Solicitacoes()
        solicitacao_to_db.id = solicitacao_from_domain.id
        solicitacao_to_db.titulo = solicitacao_from_domain.titulo
        solicitacao_to_db.descricao = solicitacao_from_domain.descricao
        solicitacao_to_db.status = solicitacao_from_domain.status.name
        solicitacao_to_db.data_criacao = solicitacao_from_domain.data_criacao
        solicitacao_to_db.contrato_id = contrato_id

        return solicitacao_to_db
