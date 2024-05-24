from datetime import datetime
from typing import List
from uuid import UUID

from domain.enums.status import Status
from domain.models.contrato import Contrato
from domain.models.imovel import Imovel
from domain.models.locatario import Locatario
from domain.models.ocorrencia import Ocorrencia
from domain.models.solicitacao import Solicitacao
from infrastructure.models.ocorrencias import Ocorrencias
from infrastructure.models.solicitacoes import Solicitacoes


class ContratoInputMapper:
    @staticmethod
    def map_contrato(contrato, solicitacoes: List[Solicitacoes], locatario: Locatario, imovel: Imovel,
                     ocorrencias: List[Ocorrencias], vistorias):
        lista_solicitacoes = []
        lista_ocorrencias = []
        for solicitacao in solicitacoes:
            lista_solicitacoes.append(Solicitacao(id=UUID(solicitacao.id),
                                                  titulo=solicitacao.titulo,
                                                  descricao=solicitacao.descricao,
                                                  status=Status(solicitacao.status),
                                                  data_criacao=datetime.strptime(solicitacao.data_criacao, "%d/%m/%Y")))

        for ocorrencia in ocorrencias:
            lista_ocorrencias.append(Ocorrencia(id=UUID(ocorrencia.id),
                                                titulo=ocorrencia.titulo,
                                                descricao=ocorrencia.descricao,
                                                status=Status(ocorrencia.status),
                                                data_criacao=datetime.strptime(ocorrencia.data_criacao, "%d/%m/%Y")))

        locatario = Locatario(email=locatario.email,
                              senha=locatario.senha,
                              nome=locatario.nome,
                              data_nascimento=locatario.data_nascimento,
                              id=locatario.id)
        imovel = Imovel(id=imovel.id,
                        codigo=imovel.codigo,
                        endereco=imovel.endereco,
                        imagens=imovel.imagens,)

        contrato = Contrato(id=UUID(contrato.id),
                            dataInicio=contrato.data_inicio,
                            locatario=locatario,
                            imovel=imovel,
                            estaAtivo=contrato.estaAtivo,
                            vistoria_inicial=contrato.vistoria_inicial,
                            criador=contrato.criador,
                            dataFim=contrato.data_fim,)
