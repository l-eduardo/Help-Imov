from datetime import datetime

from application.controllers.chat_controller import ChatCrontroller
from application.controllers.usuarios_controller import UsuariosController
from application.controllers.session_controller import SessionController
from domain.enums.status import Status
from domain.models.Imagem import Imagem
from domain.models.session import Session
from infrastructure.repositories.prestadores_servicos_repository import PrestadoresServicosRepository
from infrastructure.repositories.chats_repository import ChatsRepository
from infrastructure.repositories.user_identity_repository import UserIdentityRepository
from infrastructure.services.Documentos_Svc import DocumentosService
from infrastructure.services.Imagens_Svc import ImagensService
from presentation.components.validations_errors_popup import ValidationErrorsPopup
from presentation.views.contrato_view import TelaContrato
from presentation.views.ocorrencia_view import OcorrenciaView
from presentation.views.solicitacao_view import SolicitacaoView
from presentation.views.vistoria_view import TelaVistoria
from domain.models.contrato import Contrato
from domain.models.contrato import Chat
from domain.models.vistoria import Vistoria
from infrastructure.repositories.contratos_repository import ContratosRepositories
from infrastructure.repositories.ocorrencias_repository import OcorrenciasRepository
from infrastructure.repositories.solicitacoes_repository import SolicitacoesRepository
from infrastructure.repositories.vistorias_repository import VistoriasRepository
from infrastructure.mappers.ContratosOutput import ContratosOutputMapper

import PySimpleGUI as sg


class ContratoController:
    def __init__(self, main_controller):
        self.__main_controller = main_controller
        self.__chat_controller = ChatCrontroller()
        self.__usuario_controller = UsuariosController()
        self.__tela_vistoria = TelaVistoria(self)

        self.__contratos_repository = ContratosRepositories()
        self.__chat_repository = ChatsRepository()
        self.__ocorrencia_repository: OcorrenciasRepository = OcorrenciasRepository()
        self.__prestadores_repository = PrestadoresServicosRepository()
        self.__solicitacao_repository = SolicitacoesRepository()
        self.__user_identity_repository = UserIdentityRepository()
        self.__vistoria_repository = VistoriasRepository()

        self.__tela_contrato = TelaContrato(self)
        self.__solicitacao_view = SolicitacaoView(self)
        self.__ocorrencia_view: OcorrenciaView = OcorrenciaView()

        self.contratos = []

    def inclui_contrato(self):
        while True:
            dados_contrato, locatario_selecionado = self.__tela_contrato.pega_dados_contrato()
            imovel = dados_contrato['imovel']
            data = dados_contrato['data_inicio']
            if self.valida_campos_contrato(imovel, locatario_selecionado, data):
                contrato = Contrato(dataInicio=dados_contrato['data_inicio'], imovel=dados_contrato['imovel'],
                                    locatario=locatario_selecionado, estaAtivo=True)
                self.__contratos_repository.insert(ContratosOutputMapper.map_contrato(contrato))
                self.__tela_contrato.mostra_msg('Contrato Criado com sucesso')
                break
        self.listar_contrato()

    @SessionController.inject_session_data
    def listar_contrato(self, session: Session=None):
        contrato_instancia = None
        self.contratos = self.obter_contratos_do_banco()
        btn_visible_locatario = True
        if session.user_role == "Locatario":
            btn_visible_locatario = False
        contratos_listados = []
        for contrato in self.contratos:
            if session.user_id == contrato.locatario.id:
                if contrato.estaAtivo:
                    contratos_listados.append(contrato)
            if session.user_role in ["Administrador", "Assistente"]:
                contratos_listados = self.obter_contratos_do_banco()

        event, values, btn_visible_locatario = self.__tela_contrato.mostra_contratos(contratos_listados, btn_visible_locatario)
        if event == "Visualizar":
            if values["-TABELA-"]:
                contrato_selecionado = contratos_listados[values["-TABELA-"][0]]
                self.selecionar_contrato(contrato_selecionado, btn_visible_locatario)

            else:
                sg.popup("Nenhum contrato selecionado")
        if event == "Adicionar":
            self.inclui_contrato()
        if event == "Selecionar":
            contrato_selecionado = contratos_listados[values["-TABELA-"][0]]
            for contrato in self.contratos:
                if contrato_selecionado.id == contrato.id:
                    contrato_instancia = contrato
                    break
            self.listar_relacionados_contrato(contrato_instancia)
            return contrato_selecionado

    def selecionar_contrato(self, contrato_selecionado: Contrato, btn_visible_locatario):
        contrato, _ = self.__tela_contrato.mostra_contrato(contrato_selecionado, btn_visible_locatario)
        self.__contratos_repository.update_contrato(contrato)
        self.listar_contrato()

    def obter_contratos_do_banco(self) -> list[Contrato]:
        contratos = self.__contratos_repository.get_all()
        return contratos

    def get_id_contratos(self):
        return [contrato.id for contrato in self.contratos]

    @SessionController.inject_session_data
    def listar_relacionados_contrato(self, contrato_instancia: Contrato, session: Session = None):
        if contrato_instancia is None:
            self.__tela_contrato.mostra_msg("Nenhum contrato selecionado")
            return

        ocorrencias_para_tela = []
        for ocorrencia in contrato_instancia.ocorrencias:
            ocorrencias_para_tela.append({
                "tipo": "Ocorrência",
                "titulo": ocorrencia.titulo,
                "status": ocorrencia.status.value,
                "dataCriacao": ocorrencia.data_criacao,
                "prestador_id": ocorrencia.prestador_id,
                "entity": ocorrencia
            })

        solicitacoes_para_tela = []
        for solicitacao in contrato_instancia.solicitacoes:
            solicitacoes_para_tela.append({
                "tipo": "Solicitação",
                "titulo": solicitacao.titulo,
                "status": solicitacao.status.value,
                "dataCriacao": solicitacao.data_criacao,
                "entity": solicitacao
            })

        solicitacoes_ocorrencias = ocorrencias_para_tela + solicitacoes_para_tela

        if solicitacoes_ocorrencias:
            events, values, contrato = self.__tela_contrato.mostra_relacionados_contrato(solicitacoes_ocorrencias,
                                                                                         contrato_instancia)
        else:
            self.__tela_contrato.mostra_msg("Não há solicitações ou ocorrências cadastradas neste contrato")
            events, values, contrato = self.__tela_contrato.mostra_relacionados_contrato(solicitacoes_ocorrencias,
                                                                                         contrato_instancia)

        if events == "add_ocorrencia":
            event, values = self.__ocorrencia_view.vw_nova_ocorrencia()
            if event == "Salvar":
                imagens = ImagensService.bulk_read(values['imagens'])
                errors = contrato_instancia.incluir_ocorrencia(values["titulo"], values["descricao"], session.user_id,
                                                               imagens=imagens, prestador_id=None)

                if len(errors) > 0:
                    ValidationErrorsPopup.show_errors(errors)
                else:
                    self.__ocorrencia_repository.insert(ocorrencia=contrato_instancia.ocorrencias[-1],
                                                        contrato_id=contrato_instancia.id)

        elif events == "add_solicitacao":
            while True:
                event, values = self.__solicitacao_view.pega_dados_solicitacao()
                titulo = values["titulo"]
                descricao = values["descricao"]
                if event == "Registrar":
                    if self.validar_campos_entidade(titulo, descricao):
                        contrato_instancia.incluir_solicitacao(titulo, descricao, session.user_id)
                        self.__solicitacao_repository.insert(solicitacao=contrato_instancia.solicitacoes[-1],
                                                             id_contrato=contrato_instancia.id)
                        self.__solicitacao_view.mostra_msg("Solicitação registrada com sucesso")
                        break  # Sai do loop se validar os dados
                else:
                    break  # Sai do loop se clica em cancelar

        elif events == "Excluir" and values["-TABELA-"] is not None:
            entidade = solicitacoes_ocorrencias[values["-TABELA-"][0]]
            if entidade["entity"].criador_id != session.user_id:
                self.__ocorrencia_view.mostra_popup("Você não tem permissão para excluir esta ocorrência/solicitacao")
            elif entidade["tipo"] == "Ocorrência":
                contrato_instancia.remover_ocorrencia(entidade["entity"])
                self.__ocorrencia_repository.delete(entidade["entity"].id)
            elif entidade["tipo"] == "Solicitação":
                contrato_instancia.remover_solicitacao(entidade["entity"])
                self.__solicitacao_repository.delete(entidade["entity"].id)

        elif events == "-TABELA-DOUBLE-CLICK-":
            entidade = solicitacoes_ocorrencias[values["-TABELA-"][0]]
            if entidade["tipo"] == "Ocorrência":
                imagens_dir = ImagensService.bulk_local_temp_save(entidade["entity"].imagens)
                mostra_ocorr_event, _ = self.__ocorrencia_view.vw_mostra_ocorrencia(entidade["entity"],
                                                                dirs=imagens_dir)
                if entidade["entity"].criador_id != session.user_id:
                    sg.popup("Você não tem permissão para editar esta ocorrência")
                elif mostra_ocorr_event == "editar_ocorrencia":
                    editar_ocorr_events, editar_ocorr_values = self.__ocorrencia_view.vw_editar_ocorrencia(
                        entidade["entity"])
                    if editar_ocorr_events == "confirmar_edicao":
                        titulo = editar_ocorr_values["titulo"]
                        descricao = editar_ocorr_values["descricao"]
                        prestador_id = editar_ocorr_values.get("prestadores")
                        if self.validar_campos_entidade(titulo, descricao):
                            entidade["entity"].titulo = editar_ocorr_values["titulo"]
                            entidade["entity"].descricao = editar_ocorr_values["descricao"]
                            entidade["entity"].status = Status(editar_ocorr_values["status"])
                            entidade["entity"].prestador_id = prestador_id
                            self.__ocorrencia_repository.update(entidade["entity"])

                elif mostra_ocorr_event == "Chat":
                    chat = entidade["entity"].chat
                    if not isinstance(chat, Chat):
                        chat = entidade["entity"].incluir_chat()
                        self.__chat_repository.insert_chat(chat)

                    usuario_logado_id = session.user_id
                    usuario_logado = self.__usuario_controller.usuario_by_id(usuario_logado_id)
                    self.__chat_controller.mostra_chat(usuario_logado=usuario_logado, chat=chat)

            if entidade["tipo"] == "Solicitação":
                while True:
                    event_solic, _ = self.__solicitacao_view.mostra_solicitacao(entidade["entity"])
                    if entidade["entity"].criador_id != session.user_id:
                        sg.popup("Você não tem permissão para editar esta solicitação")
                    elif event_solic == "editar_solicitacao":
                        while True:
                            edit_solic_events, edit_solic_values = self.__solicitacao_view.editar_solicitacao(entidade["entity"])
                            titulo = edit_solic_values["titulo"]
                            descricao = edit_solic_values["descricao"]
                            if edit_solic_events == "confirmar_edicao":
                                if self.validar_campos_entidade(titulo, descricao):
                                    entidade["entity"].titulo = edit_solic_values["titulo"]
                                    entidade["entity"].descricao = edit_solic_values["descricao"]
                                    entidade["entity"].status = Status(edit_solic_values["status"])
                                    self.__solicitacao_repository.update(entidade["entity"])
                                break
                    break

        if events == "vistoria_inicial":
            if contrato_instancia.vistoria_inicial:
                caminho_documento = DocumentosService.save_file(contrato_instancia.vistoria_inicial.documento)
                vistoria_result = self.__tela_vistoria.mostra_vistoria(vistoria=contrato_instancia.vistoria_inicial,
                                                     lista_paths_imagens=ImagensService.bulk_local_temp_save(contrato_instancia.vistoria_inicial.imagens),
                                                     caminho_documento=caminho_documento,
                                                     e_contestacao = False,
                                                     user_role=session.user_role)
                if vistoria_result is not None:
                    event, vistoria = vistoria_result

                    if event == "editar_vistoria":
                        if vistoria.esta_fechada():
                            sg.Popup("Vistoria não pode ser excluida ou editada pois ja atingiu o prazo maximo de 14 dias")
                        else:
                            self.editar_vistoria(contrato_instancia, vistoria)
                    elif event == "excluir_vistoria":
                        if vistoria.esta_fechada():
                            sg.Popup("Vistoria não pode ser excluida ou editada pois ja atingiu o prazo maximo de 14 dias")
                        else:
                            contrato_instancia.remover_vistoria(vistoria)
                            self.__vistoria_repository.delete(vistoria.id)
                            sg.popup("Contestação de vistoria excluida com sucesso", title="Aviso")
            else:
                if session.user_role == 'Locatario':
                    sg.popup("Não há vistoria inicial cadastrada ainda.\n\nVocê não possui permissão para criá-la")
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
                                                     lista_paths_imagens=ImagensService.bulk_local_temp_save(contrato_instancia.contra_vistoria.imagens),
                                                     caminho_documento=caminho_documento,
                                                     e_contestacao=True,
                                                     user_role=session.user_role)
                if vistoria_result is not None:
                    event, vistoria = vistoria_result
                    if event == "editar_vistoria":
                        if vistoria.esta_fechada():
                            sg.Popup("Vistoria não pode ser excluida ou editada pois ja atingiu o prazo maximo de 14 dias")
                        else:
                            self.editar_vistoria(contrato_instancia, vistoria)
                    elif event == "excluir_vistoria":
                        if vistoria.esta_fechada():
                            sg.Popup("Vistoria não pode ser excluida ou editada pois ja atingiu o prazo maximo de 14 dias")
                        else:
                            contrato_instancia.remover_vistoria(vistoria)
                            self.__vistoria_repository.delete(vistoria.id)
                            sg.popup("Contestação de vistoria excluida com sucesso", title="Aviso")
            else:
                if contrato_instancia.esta_fechada():
                    sg.popup(
                        "Vistoria não pode ser incluida pois ja atingiu o prazo maximo de 14 dias",
                        title="Aviso",
                        custom_text="Fechar"
                    )
                else:
                    criar_contra_vistoria = sg.popup(
                        "Não existe Contra-Vistoria cadastrada",
                        title="Aviso",
                        custom_text=("Criar", "Fechar")
                    )
                    if criar_contra_vistoria == "Criar":
                            self.incluir_vistoria(contrato_instancia, e_contestacao = True)

        elif events == "Voltar":
            ImagensService.flush_temp_images()
            self.listar_contrato()

        elif events == sg.WIN_CLOSED:
            ImagensService.flush_temp_images()
            return
        self.listar_relacionados_contrato(contrato_instancia)

    def incluir_vistoria(self, contrato: Contrato, e_contestacao):
        event, values = self.__tela_vistoria.pega_dados_vistoria()
        if event == "Registrar":
            try:
                imagens = ImagensService.bulk_read(values['imagens'].split(';'))
                imagens_invalidas = [imagem for imagem in imagens if not imagem.e_valida()]

                if imagens_invalidas and len(imagens_invalidas):
                    self.__tela_vistoria.mostra_msg(
                        "Imagens inválidas. Por favor, selecione imagens com resolucao entre 1280x720 e 1820x1280 pixels!")

                else:
                    contrato.incluir_vistoria(descricao=values["descricao"],
                                            imagens=imagens,
                                            documento=DocumentosService.read_file(values["documento"]),
                                            e_contestacao=e_contestacao)
                    vistoria_to_insert = contrato.contra_vistoria if e_contestacao else contrato.vistoria_inicial
                    self.__vistoria_repository.insert(vistoria=vistoria_to_insert)
                    self.__contratos_repository.update(contrato)
            except:
                sg.popup("Algo deu errado, tente novamente. \n\nLembre-se que todos os dados são necessários!")

    def editar_vistoria(self, contrato_instancia, vistoria):
        event, values = self.__tela_vistoria.pega_dados_editar_vistoria(vistoria)
        if event == "Salvar":
            vistoria.descricao = values["descricao"]
            self.__vistoria_repository.update(vistoria)
            sg.popup("Vistoria atualizada com sucesso", title="Sucesso")
        elif event == "Cancelar":
            sg.popup("Edição cancelada", title="Aviso")

        self.listar_relacionados_contrato(contrato_instancia)

    def validar_campos_entidade(self, titulo, descricao):
        if not titulo or not descricao:
            sg.popup("Todos os campos devem ser preenchidos.")
            return False
        if len(titulo) > 25:
            sg.popup("O título não pode exceder 25 caracteres.")
            return False
        if len(descricao) > 500:
            sg.popup("A descrição não pode exceder 500 caracteres.")
            return False
        return True

    def valida_campos_contrato(self, imovel, locatario, data):
        if imovel == "Selecione":
            sg.popup("Selecione um imóvel")
            return False
        if locatario is None:
            sg.Popup("Selecione um locatário")
            return False
        if data == '':
            sg.Popup("Selecione uma data")
            return False
        return True
