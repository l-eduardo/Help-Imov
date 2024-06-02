from application.controllers.session_controller import SessionController

from domain.models.imovel import Imovel
from domain.models.session import Session
from infrastructure.repositories.imoveis_repository import ImoveisRepository
from infrastructure.services.Imagens_Svc import ImagensService
from presentation.views.imovel_view import TelaImovel
from infrastructure.mappers.ImovelOutput import ImovelOutputMapper
import PySimpleGUI as sg


class ImoveisController:
    def __init__(self, controlador_sistema):
        self.controlador_sistema = controlador_sistema
        self.__imoveis_repository = ImoveisRepository()
        self.__tela_imovel = TelaImovel(self)
        self.imoveis = []
        self.contratos = []
        from application.controllers.contrato_controller import ContratoController

    def inclui_imovel(self):
        event, values = self.__tela_imovel.pega_dados_imovel()
        if event == "Registrar":
            try:
                imovel = Imovel(codigo=values['codigo'], endereco=values['endereco'],
                                imagens=ImagensService.bulk_read(values["imagens"].split(';')))
                self.__imoveis_repository.insert(imovel)
                self.__imoveis_repository.update(imovel)
                self.listar_imoveis()
            except:
                sg.Popup("Algo deu errado, tente novamente. \n\nLembre-se que todos os dados são necessários!")


    def editar_imovel(self, imovel):
        # Encontra e substitui o imóvel pelo novo
        for idx, item in enumerate(self.imoveis):
            if item.codigo == imovel.codigo:
                self.imoveis[idx] = imovel
                break

    def excluir_imovel(self, imovel: Imovel):
        # Exclui um imóvel da lista
        if self.contrato_associado(imovel.id):
            self.__tela_imovel.mostra_msg("Imovel associado a um contrato. Não é possivel excluir")
        else:
            self.imoveis.remove(imovel)
            self.__imoveis_repository.delete(imovel.id)

    def contrato_associado(self, imovel_id):
        # Importe localmente dentro do método
        from application.controllers.contrato_controller import ContratoController

        contratos_controller = ContratoController(self)
        self.contratos = contratos_controller.obter_contratos_do_banco()
        for contrato in self.contratos:
            if contrato.imovel.id == imovel_id:
                return True
        return False


    def buscar_imovel_por_codigo(self, codigo):
        # Busca um imóvel pelo código
        for item in self.imoveis:
            if item.codigo == codigo:
                return item
        return None

    def obter_imoveis_do_banco(self) -> list[Imovel]:
        imoveis = self.__imoveis_repository.get_all()
        return imoveis

    def get_id_imoveis(self):
        return [imovel.id for imovel in self.imoveis]

    def listar_imoveis(self):
        while True:
            self.imoveis = self.obter_imoveis_do_banco()
            imoveis_listados = []
            for imovel in self.imoveis:
                imoveis_listados.append({
                    "idImovel": imovel.id,
                    "codigo": imovel.codigo,
                    "endereco": imovel.endereco,
                    "imagem": imovel.imagens,
                    "entity": imovel
                })

            event, values = self.__tela_imovel.mostra_imoveis_lista(imoveis_listados)

            if event == "Visualizar":
                if values["-TABELA-"]:
                    # Pega o índice do imóvel selecionado
                    entidade = imoveis_listados[values["-TABELA-"][0]]

                    img_dir = ImagensService.bulk_local_temp_save(entidade["imagem"])
                    imovel_result = self.__tela_imovel.mostra_imovel(
                                entidade["entity"],
                                lista_paths_imagens=img_dir)


                    if imovel_result is not None:
                        event, imovel = imovel_result
                        if event == "editar_imovel":
                            self.editar_imovel(imovel)
                        if event == "excluir_imovel":
                            self.excluir_imovel(imovel)
                            self.__imoveis_repository.delete(imovel)
                        if event == "voltar":
                            continue
                else:
                    sg.Popup("Nenhum imóvel selecionado")

            if event == "Adicionar":
                self.inclui_imovel()

            if event in (sg.WIN_CLOSED, "Voltar"):
                break

    def obter_detalhes_imovel(self, id_imovel):
        for imovel in self.imoveis:
            if imovel.id == id_imovel:
                return imovel
        return None
