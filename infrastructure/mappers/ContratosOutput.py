from domain.models.contrato import Contrato
from infrastructure.models.contratos import Contratos
from datetime import datetime

class ContratosOutputMapper:
    @staticmethod
    def map_contrato(contrato: Contrato) -> Contratos:
        return Contratos(
            id=str(contrato._id),
            #data_inicio=datetime.strptime(contrato.dataInicio, "%d/%m/%Y"),
            data_inicio=contrato.dataInicio,
            data_fim=contrato.dataFim,
            data_cadastro=contrato.dataCadastro,
            #locatario_id=contrato.locatario,
            locatario_id="202020",
            #imovel_id=contrato.imovel.id,
            imovel_id='e7c3de8c-114d-4eee-a163-9306661ac7a7',
            #vistoria_inicial=contrato._vistoria_inicial.id,
            vistoria_inicial_id=None,
            contestecao_vistoria_inicial_id=None,
            #estaAtivo=contrato.estaAtivo
        )
