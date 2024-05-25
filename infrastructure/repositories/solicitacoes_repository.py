from uuid import UUID
from domain.models.solicitacao import Solicitacao
from infrastructure.configs.connection import Connection
from infrastructure.mappers.SolicitacaoOutput import SolicitacaoOutputMapper
from infrastructure.models.solicitacoes import Solicitacoes


class SolicitacoesRepository:
    def insert(self, solicitacao: Solicitacao, contrato_id: UUID) -> Solicitacao:
        solicitacao_to_db = SolicitacaoOutputMapper.map_solicitacao(solicitacao_from_domain=solicitacao, contrato_id=contrato_id)

        with Connection() as connection:
            connection.session.add(solicitacao_to_db)
            connection.session.commit()
            return solicitacao

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            connection.session.query(Solicitacoes).filter(Solicitacoes.id == id).delete()

