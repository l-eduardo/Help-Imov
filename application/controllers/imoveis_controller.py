# imoveis_controller.py
from domain.models.imovel import Imovel
from infrastructure.repositories.imoveis_repository import ImoveisRepository


class ImoveisController:
    def __init__(self):
        # Inicializar a lista de imóveis e contratos
        self.__imoveis_repository = ImoveisRepository()
        self.contratos = {}

    def adicionar_imovel(self, imovel):
        # Adiciona um imóvel à lista
        self.imoveis.append(imovel)

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

    def obter_imoveis_do_banco(self):
        imoveis = self.__imoveis_repository.get_all()
        return imoveis

    def get_codigos_imoveis(self):
        return [imovel.codigo for imovel in self.imoveis]
