from datetime import datetime
import subprocess, os, platform

from application.controllers.session_controller import SessionController
from domain.enums.status import Status
from domain.models.Imagem import Imagem
from domain.models.session import Session
from infrastructure.services.Documentos_Svc import DocumentosService
from infrastructure.services.Imagens_Svc import ImagensService
from presentation.views.contrato_view import TelaContrato
from presentation.views.ocorrencia_view import OcorrenciaView
from presentation.views.solicitacao_view import SolicitacaoView
from presentation.views.vistoria_view import TelaVistoria
from domain.models.contrato import Contrato
from domain.models.vistoria import Vistoria
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
        #TODO Inclusao contrato
        dados_contrato = self.__tela_contrato.pega_dados_contrato()
        contrato = Contrato(dataInicio=dados_contrato['data_inicio'], imovel=dados_contrato['imovel'],
                            locatario=dados_contrato['locatario'], estaAtivo=True)
        self.__contratos_repository.insert(ContratosOutputMapper.map_contrato(contrato))
        self.listar_contrato()
        #self.__tela_contrato.mostra_msg('Contrato Criado com sucesso')

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

    @SessionController.inject_session_data
    def listar_relacionados_contrato(self, contrato_instancia: Contrato, session: Session=None):
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
                contrato_instancia.incluir_ocorrencia(values["titulo"],
                                                      values["descricao"],
                                                      session.user_id,
                                                      imagens=[])

                self.__ocorrencia_repository.insert(ocorrencia=contrato_instancia.ocorrencias[-1],
                                                    contrato_id=contrato_instancia.id)

        elif events == "add_solicitacao":
            event, values = self.__solicitacao_view.pega_dados_solicitacao()
            if event == "Registrar":
                contrato_instancia.incluir_solicitacao(values["titulo"], values["descricao"], session.user_id)
                self.__solicitacao_repository.insert(solicitacao=contrato_instancia.solicitacoes[-1],
                                                     id_contrato=contrato_instancia.id)

        elif events == "Excluir" and values["-TABELA-"] is not None:
            entidade = solicitacoes_ocorrencias[values["-TABELA-"][0]]

            if entidade["entity"].criador_id != session.user_id:
                sg.popup("Você não tem permissão para excluir esta ocorrência")

            elif entidade["tipo"] == "Ocorrência":
                contrato_instancia.remover_ocorrencia(entidade["entity"])
                self.__ocorrencia_repository.delete(entidade["entity"].id)

            elif entidade["tipo"] == "Solicitação":
                contrato_instancia.remover_solicitacao(entidade["entity"])
                self.__solicitacao_repository.delete(entidade["entity"].id)

        elif events == "-TABELA-DOUBLE-CLICK-":
            entidade = solicitacoes_ocorrencias[values["-TABELA-"][0]]
            if entidade["tipo"] == "Ocorrência":
                mostra_ocorr_event, _ = self.__ocorrencia_view.vw_mostra_ocorrencia(entidade["entity"])

                if entidade["entity"].criador_id != session.user_id:
                    sg.popup("Você não tem permissão para editar esta ocorrência")

                elif mostra_ocorr_event == "editar_ocorrencia":
                    editar_ocorr_events, editar_ocorr_values = self.__ocorrencia_view.vw_editar_ocorrencia(entidade["entity"])

                    if editar_ocorr_events == "confirmar_edicao":
                        entidade["entity"].titulo = editar_ocorr_values["titulo"]
                        entidade["entity"].descricao = editar_ocorr_values["descricao"]
                        entidade["entity"].status = Status(editar_ocorr_values["status"])
                        self.__ocorrencia_repository.update(entidade["entity"])

            elif entidade["tipo"] == "Solicitação":
                event_solic, _ = self.__solicitacao_view.mostra_solicitacao(entidade["entity"])

                if entidade["entity"].criador_id != session.user_id:
                    sg.popup("Você não tem permissão para editar esta solicitacao")

                if event_solic == "editar_solicitacao":
                    edit_solic_events, edit_solic_values = self.__solicitacao_view.editar_solicitacao(entidade["entity"])

                    if edit_solic_events == "confirmar_edicao":
                        print(edit_solic_events)
                        entidade["entity"].titulo = edit_solic_values["titulo"]
                        entidade["entity"].descricao = edit_solic_values["descricao"]
                        entidade["entity"].status = Status(edit_solic_values["status"])
                        self.__solicitacao_repository.update(entidade["entity"])

        if events == "vistoria_inicial":
            if contrato_instancia.vistoria_inicial:
                caminho_documento = DocumentosService.save_file(contrato_instancia.vistoria_inicial.documento)
                vistoria_result = self.__tela_vistoria.mostra_vistoria(vistoria=contrato_instancia.vistoria_inicial,
                                                     lista_paths_imagens=ImagensService.bulk_local_temp_save(contrato_instancia.vistoria_inicial.imagens))
                if vistoria_result is not None:
                    event, vistoria = vistoria_result

                    if event == "editar_vistoria":
                        # if Vistoria.esta_fechada(vistoria) == False: implementar depois
                            self.editar_vistoria(contrato_instancia, vistoria)
                    elif event == "excluir_vistoria":
                        contrato_instancia.remover_vistoria(vistoria)
                        self.__vistoria_repository.delete(vistoria.id)
                        sg.popup("Contestação de vistoria excluida com sucesso", title="Aviso")
                    elif event == "abrir_documento":
                        self.abrir_documento(caminho_documento)
            else:
                criar_contra_vistoria = sg.popup(
                    "Não existe Vistoria Inicial cadastrada",
                    title="Aviso",
                    custom_text=("Criar", "Fechar")
                )
                if criar_contra_vistoria == "Criar":
                    self.incluir_vistoria(contrato_instancia, e_contestacao = False)

        if events == "contra_vistoria":
            if contrato_instancia.contra_vistoria:
                caminho_documento = DocumentosService.save_file(contrato_instancia.contra_vistoria.documento) 
                vistoria_result = self.__tela_vistoria.mostra_vistoria(vistoria=contrato_instancia.contra_vistoria,
                                                     lista_paths_imagens=ImagensService.bulk_local_temp_save(contrato_instancia.contra_vistoria.imagens))
                if vistoria_result is not None:
                    event, vistoria = vistoria_result
                    if event == "editar_vistoria":
                        self.editar_vistoria(contrato_instancia, vistoria)
                    elif event == "excluir_vistoria":
                        if vistoria.esta_fechada():
                            sg.Popup("Vistoria não pode ser excluida ou editada pois ja atingiu o prazo maximo de 14 dias")
                        else:
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

        elif events == "Voltar":
            self.listar_contrato()

        elif events == sg.WIN_CLOSED:
            return
        self.listar_relacionados_contrato(contrato_instancia)


    def incluir_vistoria(self, contrato: Contrato, e_contestacao):
        event, values = self.__tela_vistoria.pega_dados_vistoria()
        if event == "Registrar":
            contrato.incluir_vistoria(descricao=values["descricao"],
                                      imagens=ImagensService.bulk_read(values["imagens"].split(';')),
                                      documento=DocumentosService.read_file(values["documento"]),
                                      e_contestacao=e_contestacao)
            vistoria_to_insert = contrato.contra_vistoria if e_contestacao else contrato.vistoria_inicial
            self.__vistoria_repository.insert(vistoria=vistoria_to_insert, # colocar depois uma verificação pra mudar pra vistoria_inicial
                                                id_contrato=contrato.id)
            self.__contratos_repository.update(contrato)
        else:
            sg.popup("A vistoria não foi criada", title="Aviso")

    def editar_vistoria(self, contrato_instancia, vistoria):
        event, values = self.__tela_vistoria.pega_dados_editar_vistoria(vistoria)
        if event == "Salvar":
            vistoria.descricao = values["descricao"]
            # vistoria.imagens = [Imagem(caminho=img_path) for img_path in values["imagens"].split(";")]
            # vistoria.documento = values["documento"]
            self.__vistoria_repository.update(vistoria)
            sg.popup("Vistoria atualizada com sucesso", title="Sucesso")
        elif event == "Cancelar":
            sg.popup("Edição cancelada", title="Aviso")

        self.listar_relacionados_contrato(contrato_instancia)
    
    def abrir_documento(self, caminho_documento):
        try:
            if platform.system() == 'Darwin':       # macOS
                teste = subprocess.call(('open', caminho_documento))
            elif platform.system() == 'Windows':    # Windows
                teste = os.startfile(caminho_documento)
            else:                                   # linux variants
                teste = subprocess.call(('xdg-open', caminho_documento))
            if teste == 1:
                raise ValueError("Não há programa padrão para abrir, abrindo diretório")
        except:
            caminho_documento = caminho_documento.replace(caminho_documento.split('/')[-1],"")
            if platform.system() == 'Darwin':       # macOS
                teste = subprocess.call(('open', caminho_documento))
            elif platform.system() == 'Windows':    # Windows
                teste = os.startfile(caminho_documento)
            else:                                   # linux variants
                teste = subprocess.call(('xdg-open', caminho_documento))
