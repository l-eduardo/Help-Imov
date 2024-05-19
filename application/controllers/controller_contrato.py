from presentation.views.contrato_view import TelaContrato
from domain.models.contrato import Contrato
from infrastructure.repositories.contratos_repository import ContratosRepositories
from infrastructure.mappers.ContratosOutput import ContratosOutputMapper
from uuid import UUID


class ContratoController:
    def __init__(self, controlador_sistema):
        self.__contratos_repository = ContratosRepositories()
        self.__tela_contrato = TelaContrato(self)
        self.__controlador_sistema = controlador_sistema

        self.contratos = self.obter_contratos_do_banco()
        #self.imoveis = self.ImovelRepositores.get_all()

    def buscar_contratos(self):
        contratos = 0
        # Buscar da base de dados
        return self.contratos

    def inclui_contrato(self):
        dados_contrato = self.__tela_contrato.PegaDadosContrato()
        print(dados_contrato)
        contrato = Contrato(dados_contrato['data_inicio'], dados_contrato['imovel'],
                            dados_contrato['locatario'], estaAtivo=True)
        self.__contratos_repository.insert(ContratosOutputMapper.map_contrato(contrato))


        self.__tela_contrato.mostra_msg('Contrato Criado com sucesso')

    def listar_contrato(self):
        contratos_listados = []
        for contratos in self.contratos:
            contratos_listados.append({"dataInicio": contratos.dataInicio, "dataFim": contratos.dataFim,
                                       "locatario": contratos.locatario, "imovel": contratos.imovel})
            if contratos_listados:
                self.__tela_contrato.mostra_contratos(contratos_listados)
            else:
                self.__tela_contrato.mostra_msg("Nenhum contrato cadastrado")

    def selecionar_contrato(self, contrato_selecionado):
        contrato_selecionado = self.__tela_contrato.mostra_contratos()

        pass


    def obter_contratos_do_banco(self):
        contrato1 = Contrato('01-01-2024', '02-03-2024', 'locatrio1', 'IMV001', True)
        contrato2 = Contrato('01-02-2024', '02-05-2024', 'locatrio2', 'IMV002', True)
        return [contrato1, contrato2]

    def get_id_contratos(self):
        return [contrato.id for contrato in self.contratos]


