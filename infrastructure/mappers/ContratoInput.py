from datetime import datetime
from typing import List
from uuid import UUID

from domain.enums.status import Status
from domain.models.contrato import Contrato
from domain.models.imovel import Imovel
from domain.models.locatario import Locatario
from domain.models.ocorrencia import Ocorrencia
from domain.models.solicitacao import Solicitacao
from infrastructure.mappers.ChatInput import ChatInputMapper
from infrastructure.mappers.DocumentoInput import DocumentoInputMapper
from infrastructure.mappers.ImagemInput import ImagemInputMapper
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
        data_cadastro=contrato_from_db.data_cadastro,
        # TODO: Vistoria inicial, terminar
        vistoria_inicial=None,
        contra_vistoria=None,
        dataFim=contrato_from_db.data_fim,
        id=UUID(contrato_from_db.id))

        for solicitacao in contrato_from_db.solicitacoes:
            contrato.incluir_solicitacao(
                titulo=solicitacao.titulo,
                descricao=solicitacao.descricao,
                status=solicitacao.status,
                data_criacao=solicitacao.data_criacao,
                criador_id=solicitacao.criador_id,
                id=UUID(solicitacao.id))

        for ocorrencia in contrato_from_db.ocorrencias:
            contrato.incluir_ocorrencia(
                titulo=ocorrencia.titulo,
                descricao=ocorrencia.descricao,
                status=ocorrencia.status,
                criador_id=ocorrencia.criador_id,
                imagens=ImagemInputMapper.bulk_map_imagens(ocorrencia.imagens),
                data_criacao=ocorrencia.data_criacao,
                prestador_id=ocorrencia.prestador_id,
                id=UUID(ocorrencia.id),
                chat=ChatInputMapper.map_chat(ocorrencia.chat) if ocorrencia.chat is not None else [])

        if contrato_from_db.vistoria_inicial is not None:
            contrato.incluir_vistoria(
                descricao=contrato_from_db.vistoria_inicial.descricao,
                imagens=ImagemInputMapper.bulk_map_imagens(contrato_from_db.vistoria_inicial.imagens),
                documento = DocumentoInputMapper.map_documento(contrato_from_db.vistoria_inicial.documento or None),
                data_criacao = contrato_from_db.vistoria_inicial.data_criacao,
                e_contestacao = False,
                id = contrato_from_db.vistoria_inicial.id
            )

        if contrato_from_db.contra_vistoria is not None:
            contrato.incluir_vistoria(
                descricao=contrato_from_db.contra_vistoria.descricao,
                imagens=ImagemInputMapper.bulk_map_imagens(contrato_from_db.contra_vistoria.imagens),
                e_contestacao = True,
                documento = DocumentoInputMapper.map_documento(contrato_from_db.contra_vistoria.documento or None),
                data_criacao = contrato_from_db.contra_vistoria.data_criacao,
                id = contrato_from_db.contra_vistoria.id
            )

        return contrato
