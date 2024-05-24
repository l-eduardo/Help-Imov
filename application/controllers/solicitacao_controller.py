# controller_solicitacao.py
from domain.models.solicitacao import Solicitacao
from presentation.views.solicitacao_view import TelaSolicitacao


class SolicitacaoController:
    def __init__(self, controlador_sistema):
        self.__tela_solicitacao = TelaSolicitacao(self)
        self.__controlador_sistema = controlador_sistema
        self.solicitacoes = self.obter_solicitacoes()


    def incluir_solicitacao(self):
        pass

    def obter_solicitacoes(self):
        pass

    def get_codigos_solicitacoes(self):
        return [solicitacao.codigo for solicitacao in self.solicitacoes]

    def selecionar_solicitacao(self, solicitacao):
        # Aqui você adiciona a lógica para processar a solicitação selecionada
        print('Solicitação selecionada:', solicitacao.codigo, solicitacao.contrato.codigo, solicitacao.descricao, solicitacao.data_solicitacao)
