from typing import List
#import mysql.connector
from domain.models.imovel import Imovel
from domain.models.locatario import Locatario
from presentation.contrato_view import ContratoScreen, ListaContratosScreen, ScreenManager
from domain.models.contrato import Contrato
from uuid import UUID
#from contratos_repository.py import ContratosRepositories
#from imovel_repository.py import ImovelRepositories


class ContratoController:
    def __init__(self, connection: mysql.connector.connection.MySQLConnection):
        self.connection = connection
        self.locatarios = self.buscar_locatarios()
        #self.imoveis = self.ImovelRepositores.get_all()
        self.screen_manager = ScreenManager()
        self.screen_contrato = ContratoScreen()
        self.screen_lista_contrato = ListaContratosScreen()


    def buscar_contratos(self):
        self.contratos = 0
        # Buscar da base de dados
        return self.contratos


    def inclui_contrato(self):
        dados_contrato = self.screen_contrato.retorna_contrato()
        novo_contrato = Contrato(dados_contrato["dataInicio"], dados_contrato["dataFim"],
                            dados_contrato["locatario"], dados_contrato["imovel"])  # JOGAR O CONTRATO PRO DB
        self.contratos.append(novo_contrato)
        self.screen_lista_contrato.update_contratos_view(self.contratos)
        print("Contrato cadastrado!")


    def get_imoveis(self):
        return [f"Código: {imovel.codigo}, Endereço: {imovel.endereco}" for imovel in self.imoveis]

    def get_locatarios(self):
        return [f"Código: {imovel.codigo}, Endereço: {imovel.endereco}" for imovel in self.imoveis]





    def buscar_imoveis(self) -> List[Imovel]:
        imoveis = 0
        return imoveis

    def buscar_locatarios(self) -> List[Locatario]:
        locatarios = 0
        return locatarios
