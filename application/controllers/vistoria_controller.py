from presentation.views.vistoria_view import TelaVistoria
from domain.models.vistoria import Vistoria
from infrastructure.repositories.vistorias_repository import VistoriasRepositories
from infrastructure.mappers.VistoriasOutput import VistoriasOutputMapper
from uuid import UUID


class VistoriaController:
    def __init__(self, controlador_sistema):
        self.__vistorias_repository = VistoriasRepositories()
        self.__tela_vistoria = TelaVistoria(self)
        self.__controlador_sistema = controlador_sistema
        self.vistorias = self.obter_vistorias_do_banco()

    def buscar_vistorias(self):
        vistorias = 0
        # Buscar da base de dados
        return self.vistorias

    def inclui_vistoria(self):
        dados_vistoria = self.__tela_vistoria.PegaDadosVistoria()
        vistoria = Vistoria(dados_vistoria['descricao'], dados_vistoria['anexos'],
                            dados_vistoria['locatario'], estaAtivo=True)
        self.__vistorias_repository.insert(VistoriasOutputMapper.map_vistoria(vistoria))


        self.__tela_vistoria.mostra_msg('Vistoria Criado com sucesso')

    def listar_vistoria(self):
        vistorias_listados = []
        for vistorias in self.vistorias:
            vistorias_listados.append({"dataInicio": vistorias.data_inicio, "dataFim": vistorias.data_inicio,
                                       "locatario": vistorias.locatario_id, "imovel": vistorias.imovel_id})
                                       #"imovel": self.__imoveis_repository.get_by_id(UUID(vistorias.imovel_id)).endereco})
        if vistorias_listados:
            self.__tela_vistoria.mostra_vistorias(vistorias_listados)
        else:
            self.__tela_vistoria.mostra_msg("Nenhum vistoria cadastrado")

    def selecionar_vistoria(self, vistoria_selecionado):
        self.__tela_vistoria.mostra_vistoria(vistoria_selecionado)

        pass

    def obter_vistorias_do_banco(self):
        vistorias = self.__vistorias_repository.get_all()
        return vistorias

        '''vistoria1 = Vistoria('01-01-2024', '02-03-2024', 'locatrio1', 'IMV001', True)
        vistoria2 = Vistoria('01-02-2024', '02-05-2024', 'locatrio2', 'IMV002', True)
        return [vistoria1, vistoria2]'''

    def get_id_vistorias(self):
        return [vistoria.id for vistoria in self.vistorias]


