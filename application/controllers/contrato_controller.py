from presentation.views.contrato_view import TelaContrato
from presentation.views.ocorrencia_view import OcorrenciaView
from presentation.views.solicitacao_view import TelaSolicitacao
from domain.models.contrato import Contrato
from infrastructure.repositories.contratos_repository import ContratosRepositories
from infrastructure.repositories.ocorrencias_repository import OcorrenciasRepository
from infrastructure.mappers.ContratosOutput import ContratosOutputMapper
import PySimpleGUI as sg

class ContratoController:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema

        self.__contratos_repository = ContratosRepositories()
        self.__ocorrencia_repository = OcorrenciasRepository()

        self.__tela_contrato = TelaContrato(self)
        self.__tela_solicitacao = TelaSolicitacao(self)
        self.__ocorrencia_view: OcorrenciaView = OcorrenciaView()

        self.contratos = []


    def inclui_contrato(self):
        #TODO Inclusao contrato
        dados_contrato = self.__tela_contrato.pega_dados_contrato()
        contrato = Contrato(dados_contrato['data_inicio'], dados_contrato['imovel'],
                            dados_contrato['locatario'], estaAtivo=True)
        instancia_contrato = self.__contratos_repository.insert(ContratosOutputMapper.map_contrato(contrato))
        print(instancia_contrato)
        #self.__tela_contrato.mostra_msg('Contrato Criado com sucesso')

    def listar_contrato(self):
        self.contratos = self.obter_contratos_do_banco()

        contratos_listados = []
        for contrato in self.contratos:
            contratos_listados.append({"idContrato": contrato.id,"dataInicio": contrato.dataInicio,
                                       "dataFim": contrato.dataFim,"locatario": contrato.locatario.id,
                                       "imovel": contrato.imovel.endereco})
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
        self.__tela_contrato.mostra_contrato(contrato_selecionado)

    def obter_contratos_do_banco(self) -> list[Contrato]:
        contratos = self.__contratos_repository.get_all()

        return contratos

    def get_id_contratos(self):
        return [contrato.id for contrato in self.contratos]

    def adiciona_solicitacao(self, contrato_instancia):

        dados_solicitacao = self.__tela_solicitacao.pega_dados_solicitacao()
        #TODO
        contrato_instancia.incluir_solicitacao(dados_solicitacao['titulo'], dados_solicitacao['descricao'])

        #TODO mostra mensagem dizendo que solicitacao foi registrada
        self.listar_relacionados_contrato(contrato_instancia)

    def listar_relacionados_contrato(self, contrato_instancia: Contrato):
        if contrato_instancia is None:
            self.__tela_contrato.mostra_msg("Nenhum contrato selecionado")
            return

        ocorrencias_para_tela = []
        for ocorrencia in contrato_instancia.ocorrencias:
            ocorrencias_para_tela.append({"tipo": "Ocorrência", "titulo": ocorrencia.titulo,
                                          "status": ocorrencia.status.value, "dataCriacao": ocorrencia.data_criacao})

        solicitacoes_para_tela = []
        for solicitacao in contrato_instancia.solicitacoes:
            solicitacoes_para_tela.append({"tipo": "Solicitação", "titulo": solicitacao.titulo,
                                          "status": solicitacao.status, "dataCriacao": solicitacao.data_criacao})

        solicitacoes_ocorrencias = ocorrencias_para_tela + solicitacoes_para_tela
        #TODO: Implementar a passagem das vistorias
        events, values, contrato = self.__tela_contrato.mostra_relacionados_contrato([], [], solicitacoes_ocorrencias,
                                                          contrato_instancia)

        if events == "add_ocorrencia":
            event, values = self.__ocorrencia_view.vw_nova_ocorrencia()

            if event == "Salvar":
                contrato_instancia.incluir_ocorrencia(values["titulo"], values["descricao"])
                self.__ocorrencia_repository.insert(ocorrencia=contrato_instancia.ocorrencias[-1],
                                                    contrato_id=contrato_instancia.id)
        if events == sg.WIN_CLOSED:
            return

        self.listar_relacionados_contrato(contrato_instancia)


