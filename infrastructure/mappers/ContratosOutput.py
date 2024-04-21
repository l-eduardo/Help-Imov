from domain.models.contrato import Contrato
from infrastructure.models.contratos import Contratos

class ContratosOutputMapper:
    @staticmethod
    def map_contrato(contrato: Contrato) -> Contratos:
        return Contratos(
            id=contrato._id,
            data_inicio=contrato.dataInicio,
            data_fim=contrato.dataFim,
            data_cadastro=contrato.dataCadastro,
            locatario=contrato.locatario.id,
            imovel=contrato.imovel.id,
            criador=contrato.criador.id,
            vistoria_inicial=contrato._vistoria_inicial.id,
            vistoria_final=None,
            estaAtivo=contrato.estaAtivo
        )
