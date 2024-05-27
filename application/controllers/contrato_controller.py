from datetime import datetime
from domain.enums.status import Status
from presentation.views.contrato_view import TelaContrato
from presentation.views.ocorrencia_view import OcorrenciaView
from presentation.views.solicitacao_view import SolicitacaoView
from presentation.views.vistoria_view import TelaVistoria
from domain.models.contrato import Contrato
from infrastructure.repositories.contratos_repository import ContratosRepositories
from infrastructure.repositories.ocorrencias_repository import OcorrenciasRepository
from infrastructure.repositories.solicitacoes_repository import SolicitacoesRepository
from infrastructure.repositories.vistorias_repository import VistoriasRepository
from infrastructure.mappers.ContratosOutput import ContratosOutputMapper
import PySimpleGUI as sg


class ContratoController:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_vistoria = TelaVistoria(self)

        self.__contratos_repository = ContratosRepositories()
        self.__ocorrencia_repository: OcorrenciasRepository = OcorrenciasRepository()
        self.__solicitacao_repository = SolicitacoesRepository()
        self.__vistoria_repository = VistoriasRepository()

        self.__tela_contrato = TelaContrato(self)
        self.__solicitacao_view = SolicitacaoView(self)
        self.__ocorrencia_view: OcorrenciaView = OcorrenciaView()

        self.contratos = []

    def inclui_contrato(self):
        dados_contrato = self.__tela_contrato.pega_dados_contrato()
        contrato = Contrato(dados_contrato['data_inicio'], dados_contrato['imovel'],
                            dados_contrato['locatario'], estaAtivo=True)
        self.incluir_vistoria(contrato, e_contestacao = False)
        self.__contratos_repository.insert(ContratosOutputMapper.map_contrato(contrato))
        self.listar_contrato()

    def listar_contrato(self):
        self.contratos = self.obter_contratos_do_banco()
        contrato_instancia = None
        contratos_listados = []
        for contrato in self.contratos:
            contratos_listados.append({"idContrato": contrato.id, "dataInicio": contrato.dataInicio,
                                       "dataFim": contrato.dataFim, "locatario": contrato.locatario.id,
                                       "imovel": contrato.imovel.endereco})
        event, values = self.__tela_contrato.mostra_contratos(contratos_listados)
        if event == "Visualizar":
            if values["-TABELA-"]:
                contrato_selecionado = contratos_listados[values["-TABELA-"][0]]
                self.selecionar_contrato(contrato_selecionado)
            else:
                sg.popup("Nenhum contrato selecionado")
        if event == "Adicionar":
            self.inclui_contrato()
        if event == "Selecionar":
            contrato_selecionado = contratos_listados[values["-TABELA-"][0]]
            for contrato in self.contratos:
                if contrato_selecionado['idContrato'] == contrato.id:
                    contrato_instancia = contrato
                    break
            self.listar_relacionados_contrato(contrato_instancia)
            return contrato_selecionado

    def selecionar_contrato(self, contrato_selecionado):
        self.__tela_contrato.mostra_contrato(contrato_selecionado)

    def obter_contratos_do_banco(self) -> list[Contrato]:
        contratos = self.__contratos_repository.get_all()
        return contratos

    def get_id_contratos(self):
        return [contrato.id for contrato in self.contratos]

    def listar_relacionados_contrato(self, contrato_instancia: Contrato):
        if contrato_instancia is None:
            self.__tela_contrato.mostra_msg("Nenhum contrato selecionado")
            return

        ocorrencias_para_tela = []
        for ocorrencia in contrato_instancia.ocorrencias:
            ocorrencias_para_tela.append({"tipo": "Ocorrência", "titulo": ocorrencia.titulo,
                                          "status": ocorrencia.status.value, "dataCriacao": ocorrencia.data_criacao,
                                          "entity": ocorrencia})
        solicitacoes_para_tela = []
        for solicitacao in contrato_instancia.solicitacoes:
            solicitacoes_para_tela.append({"tipo": "Solicitação", "titulo": solicitacao.titulo,
                                           "status": solicitacao.status.value, "dataCriacao": solicitacao.data_criacao,
                                           "entity": solicitacao})

        solicitacoes_ocorrencias = ocorrencias_para_tela + solicitacoes_para_tela

        if solicitacoes_ocorrencias:
            events, values, contrato = self.__tela_contrato.mostra_relacionados_contrato([], [],
                                                                                         solicitacoes_ocorrencias,
                                                                                         contrato_instancia)
        else:
            self.__tela_contrato.mostra_msg("Não há solicitações ou ocorrências cadastradas neste contrato")
            events, values, contrato = self.__tela_contrato.mostra_relacionados_contrato([], [],
                                                                                         solicitacoes_ocorrencias,
                                                                                         contrato_instancia)
        if events == "add_ocorrencia":
            event, values = self.__ocorrencia_view.vw_nova_ocorrencia()
            if event == "Salvar":
                contrato_instancia.incluir_ocorrencia(values["titulo"], values["descricao"])
                self.__ocorrencia_repository.insert(ocorrencia=contrato_instancia.ocorrencias[-1],
                                                    contrato_id=contrato_instancia.id)

        if events == "add_solicitacao":
            event, values = self.__solicitacao_view.pega_dados_solicitacao()
            if event == "Registrar":
                contrato_instancia.incluir_solicitacao(values["titulo"], values["descricao"])
                self.__solicitacao_repository.insert(solicitacao=contrato_instancia.solicitacoes[-1],
                                                     id_contrato=contrato_instancia.id)

        if events == "Excluir" and values["-TABELA-"] is not None:
            entidade = solicitacoes_ocorrencias[values["-TABELA-"][0]]
            if entidade["tipo"] == "Ocorrência":
                contrato_instancia.remover_ocorrencia(entidade["entity"])
                self.__ocorrencia_repository.delete(entidade["entity"].id)

        if events == "-TABELA-DOUBLE-CLICK-":
            entidade = solicitacoes_ocorrencias[values["-TABELA-"][0]]
            if entidade["tipo"] == "Ocorrência":
                mostra_ocorr_event, _ = self.__ocorrencia_view.vw_mostra_ocorrencia(entidade["entity"])

                if mostra_ocorr_event == "editar_ocorrencia":
                    editar_ocorr_events, editar_ocorr_values = self.__ocorrencia_view.vw_editar_ocorrencia(
                        entidade["entity"])

                    if editar_ocorr_events == "confirmar_edicao":
                        entidade["entity"].titulo = editar_ocorr_values["titulo"]
                        entidade["entity"].descricao = editar_ocorr_values["descricao"]
                        entidade["entity"].status = Status(editar_ocorr_values["status"])
                        self.__ocorrencia_repository.update(entidade["entity"])

            if entidade["tipo"] == "Solicitação":
                contrato_instancia.remover_solicitacao(entidade["entity"])
                self.__solicitacao_repository.delete(entidade["entity"].id)

            if entidade["tipo"] == "Solicitação":
                event_solic, _ = self.__solicitacao_view.mostra_solicitacao(entidade["entity"])
                if event_solic == "editar_solicitacao":
                    edit_solic_events, edit_solic_values = self.__solicitacao_view.editar_solicitacao(
                        entidade["entity"])
                    if edit_solic_events == "confirmar_edicao":
                        print(edit_solic_events)
                        entidade["entity"].titulo = edit_solic_values["titulo"]
                        entidade["entity"].descricao = edit_solic_values["descricao"]
                        entidade["entity"].status = Status(edit_solic_values["status"])
                        self.__solicitacao_repository.update(entidade["entity"])

        if events == "vistoria_inicial":
            if contrato_instancia.vistoria_inicial:
                self.__tela_vistoria.mostra_vistoria(contrato_instancia.vistoria_inicial)
            else:
                sg.popup("Não existe Vistoria Inicial cadastrada", title="Aviso")

        if events == "contra_vistoria":
            if contrato_instancia.contra_vistoria:
                vistoria_result = self.__tela_vistoria.mostra_vistoria(contrato_instancia.contra_vistoria)
                if vistoria_result is not None:
                    event, vistoria = vistoria_result
                    if event == "editar_vistoria":
                        pass
                    elif event == "excluir_vistoria":
                        contrato_instancia.remover_vistoria(vistoria)
                        self.__vistoria_repository.delete(vistoria.id)
                        sg.popup("Contestação de vistoria excluida com sucesso", title="Aviso")

            else:
                criar_contra_vistoria = sg.popup(
                    "Não existe Contra-Vistoria cadastrada",
                    title="Aviso",
                    custom_text=("Criar", "Fechar")
                )
                if criar_contra_vistoria == "Criar":
                    self.incluir_vistoria(contrato_instancia, e_contestacao = True)

        if events == "Voltar":
            self.listar_contrato()

        if events == sg.WIN_CLOSED:
            return
        self.listar_relacionados_contrato(contrato_instancia)

    def incluir_vistoria(self, contrato, e_contestacao):
        event, values = self.__tela_vistoria.pega_dados_vistoria()
        if event == "Registrar":
            contrato.incluir_vistoria(descricao=values["descricao"], imagens=values["imagens"].split(';'), documento=values["documento"], e_contestacao=e_contestacao)
            self.__vistoria_repository.insert(vistoria=contrato.vistoria_inicial,
                                                id_contrato=contrato.id)
        else:
            raise (KeyError)

    def valida_prazo_vistoria(self, vistoria):
        if vistoria is None:
            return False

        else:
            if (datetime.now() - vistoria.dataCadastro).days > 14:
                return False
            else:
                return True
