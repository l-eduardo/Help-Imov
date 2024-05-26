from datetime import datetime
from typing import List
from uuid import UUID

from domain.enums.status import Status
from domain.models.contrato import Contrato
from domain.models.imovel import Imovel
from domain.models.locatario import Locatario
from domain.models.ocorrencia import Ocorrencia
from domain.models.solicitacao import Solicitacao
from infrastructure.models.contratos import Contratos
from infrastructure.models.ocorrencias import Ocorrencias
from infrastructure.models.solicitacoes import Solicitacoes


class ContratoInputMapper:
    @staticmethod
    def map_contrato(contrato_from_db: Contratos):
        contrato = Contrato(contrato_from_db.data_inicio,
        locatario=contrato_from_db.locatario,
        imovel=contrato_from_db.imovel,
        estaAtivo=contrato_from_db.esta_ativo,
        # TODO: Vistoria inicial, terminar
        vistoria_inicial=None,
        dataFim=contrato_from_db.data_fim,
        id=UUID(contrato_from_db.id))

        for solicitacao in contrato_from_db.solicitacoes:
            contrato.incluir_solicitacao(
                titulo=solicitacao.titulo,
                descricao=solicitacao.descricao,
                status=solicitacao.status,
                data_criacao=solicitacao.data_criacao,
                criador_id=ocorrencia.criador_id,
                id=UUID(solicitacao.id))

        for ocorrencia in contrato_from_db.ocorrencias:
            contrato.incluir_ocorrencia(
                titulo=ocorrencia.titulo,
                descricao=ocorrencia.descricao,
                status=ocorrencia.status,
                criador_id=ocorrencia.criador_id,
                data_criacao=ocorrencia.data_criacao,
                id=UUID(ocorrencia.id))

        return contrato
