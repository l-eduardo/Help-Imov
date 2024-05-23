from domain.models import contrato
from presentation.views.contrato_view import TelaContrato
from presentation.views.solicitacao_view import TelaSolicitacao
from domain.models.contrato import Contrato
from infrastructure.repositories.contratos_repository import ContratosRepositories
from infrastructure.repositories.solicitacoes_repository import SolicitacoesRepository
from infrastructure.repositories.ocorrencias_repository import OcorrenciasRepository
from infrastructure.mappers.ContratosOutput import ContratosOutputMapper
from infrastructure.mappers.ContratoInput import ContratoInputMapper
from uuid import UUID


class ContratoController:
    def __init__(self, controlador_sistema):
        self.__contratos_repository = ContratosRepositories()
        self.__solicitacao_repository = SolicitacoesRepository()
        self.__ocorrencia_repository = OcorrenciasRepository()
        self.__tela_contrato = TelaContrato(self)
        self.__tela_solicitacao = TelaSolicitacao(self)
        self.__controlador_sistema = controlador_sistema
        self.contratos = self.obter_contratos_do_banco()
        #self.solicitacoes = self.obter_solicitacoes_do_banco()
        #self.ocorrencias = self.obter_ocorrencias_do_banco()

    def buscar_contratos(self):
        contratos = 0
        # Buscar da base de dados
        return self.contratos

    def inclui_contrato(self):
        dados_contrato = self.__tela_contrato.pega_dados_contrato()
        print(dados_contrato)
        contrato = Contrato(dados_contrato['data_inicio'], dados_contrato['imovel'],
                            dados_contrato['locatario'], estaAtivo=True)
        self.__contratos_repository.insert(ContratosOutputMapper.map_contrato(contrato))
        #self.__tela_contrato.mostra_msg('Contrato Criado com sucesso')

    def listar_contrato(self):
        contratos_listados = []
        for contrato in self.contratos:
            contratos_listados.append({"idContrato": contrato.id,"dataInicio": contrato.data_inicio,
                                       "dataFim": contrato.data_inicio,"locatario": contrato.locatario_id,
                                       "imovel": contrato.imovel_id})
        if contratos_listados:
            contrato_selecionado = self.__tela_contrato.mostra_contratos(contratos_listados)
            contrato_instancia = None
            for contrato in self.contratos:
                if contrato_selecionado["idContrato"] == contrato.id:
                    contrato_instancia = contrato
                    break
            self.listar_relacionados_contrato(contrato_instancia)
        else:
            self.__tela_contrato.mostra_msg("Nenhum contrato cadastrado")
            self.__tela_contrato.mostra_contratos(contratos_listados)

    def selecionar_contrato(self, contrato_selecionado):
        print(contrato_selecionado)
        self.__tela_contrato.mostra_contrato(contrato_selecionado)

    def obter_contratos_do_banco(self):
        contratos = self.__contratos_repository.get_all()
        solicitacoes = self.__solicitacao_repository.get_all()
        ocorrencias = self.__ocorrencia_repository.get_all()

        instancia_contratos = []

        for contrato in contratos:
            instancia_contratos.append(ContratoInputMapper.map_contrato(contrato))


        return contratos



    def obter_solicitacoes_do_banco(self):
        solicitacoes = self.__solicitacao_repository.get_all()
        return solicitacoes

    def obter_ocorrencias_do_banco(self):
        ocorrencias = self.__ocorrencia_repository.get_all()
        return ocorrencias

    def get_id_contratos(self):
        return [contrato.id for contrato in self.contratos]


    def adiciona_solicitacao(self):
        contrato = self.__tela_contrato.pega_dados_contrato()
        dados_solicitacao = self.__tela_solicitacao.pega_dados_solicitacao()
        #contrato.


    def listar_relacionados_contrato(self, contrato):
        #contrato vai ser passado pela view

        solicitacoes_ocorrencias = []
        vistoria_inicial = None
        contra_vistoria = None
        for solicitacao in contrato.solicitacoes:
            #if solicitacao.id_contrato == contrato.id:
            solicitacoes_ocorrencias.append({"tipo": solicitacao.__class__.__name__, "titulo": solicitacao.titulo,
                                            "status": solicitacao.status, "dataCriacao": solicitacao.data_criacao})

        for ocorrencia in self.ocorrencias:
            solicitacoes_ocorrencias.append({"tipo": ocorrencia.__class__.__name__, "titulo": ocorrencia.titulo,
                                            "status": ocorrencia.status, "dataCriacao": ocorrencia.data_criacao})
        self.__tela_contrato.mostra_relacionados_contrato(vistoria_inicial, contra_vistoria, solicitacoes_ocorrencias)
