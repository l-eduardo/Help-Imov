from domain.models.imovel import Imovel
from infrastructure.repositories.imoveis_repository import ImoveisRepository
from infrastructure.services.Imagens_Svc import ImagensService
from presentation.views.imovel_view import TelaImovel
from infrastructure.mappers.ImovelOutput import ImovelOutputMapper
import PySimpleGUI as sg


class ImoveisController:
    def __init__(self, controlador_sistema):
        self.contratos = None
        self.controlador_sistema = controlador_sistema
        self.__imoveis_repository = ImoveisRepository()
        self.__tela_imovel = TelaImovel(self)
        self.imoveis = []

    def inclui_imovel(self):
        dados_imovel = self.__tela_imovel.pega_dados_imovel()
        imovel = Imovel(codigo=dados_imovel['codigo'],
                        endereco=dados_imovel['endereco'],
                        imagens=ImagensService.bulk_read(dados_imovel["imagens"].split(';')))
        self.__imoveis_repository.insert(ImovelOutputMapper.map_imovel_output(imovel))

    def editar_imovel(self, imovel):
        # Encontra e substitui o imóvel pelo novo
        for idx, item in enumerate(self.imoveis):
            if item.codigo == imovel.codigo:
                self.imoveis[idx] = imovel
                break

    def excluir_imovel(self, imovel):
        # Exclui um imóvel da lista
        self.imoveis.remove(imovel)

    def contrato_associado(self, imovel_id):
        # Verifica se o imóvel tem um contrato associado
        return imovel_id in self.contratos.values()

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
        self.imoveis = self.obter_imoveis_do_banco()
        imoveis_listados = []
        for imovel in self.imoveis:
            imoveis_listados.append({
                "idImovel": imovel.id, "codigo": imovel.codigo,
                "endereco": imovel.endereco,
            })
        event, values = self.__tela_imovel.mostra_imoveis_lista(imoveis_listados)
        if event == "Visualizar":
            if values["-TABELA-"]:
                imovel_selecionado = imoveis_listados[values["-TABELA-"][0]]
                self.selecionar_imovel(imovel_selecionado)
            else:
                sg.Popup("Nenhum contrato selecionado")
        if event == "Adicionar":
            self.inclui_imovel()
        # if event == "Selecionar":
        #     imovel_selecionado = imoveis_listados[values["-TABELA-"][0]]
        #     for imovel in self.imoveis:
        #         if imovel_selecionado['idImovel'] == imovel.id:
        #             imovel_instancia = imovel
        #             break

    def selecionar_imovel(self, imovel_selecionado):
        self.__tela_imovel.mostra_imovel(imovel_selecionado)
