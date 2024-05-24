from domain.models.contrato import Contrato
from infrastructure.models.contratos import Contratos
from datetime import datetime

class ContratosOutputMapper:
    @staticmethod
    def map_contrato(contrato: Contrato) -> Contratos:
        return Contratos(
            id=contrato._id,
            #data_inicio=datetime.strptime(contrato.dataInicio, "%d/%m/%Y"),
            data_inicio=contrato.dataInicio,
            data_fim=contrato.dataFim,
            data_cadastro=contrato.dataCadastro,
            #locatario_id=contrato.locatario,
            locatario_id=4545,
            #imovel_id=contrato.imovel,
            imovel_id=4,
            funcionario_criador_id = 4545,
            #vistoria_inicial=contrato._vistoria_inicial.id,
            vistoria_inicial_id=None,
            vistoria_final_id=None,
            #estaAtivo=contrato.estaAtivo
        )
