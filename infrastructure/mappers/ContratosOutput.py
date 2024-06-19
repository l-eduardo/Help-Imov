from domain.models.contrato import Contrato
from infrastructure.models.contratos import Contratos
from datetime import datetime

class ContratosOutputMapper:
    @staticmethod
    def map_contrato(contrato: Contrato) -> Contratos:
        if contrato.vistoria_inicial is not None:
            vistoria_inicial_id = str(contrato.vistoria_inicial.id)
        else:
            vistoria_inicial_id = None

        if contrato.contra_vistoria is not None:
            contra_vistoria_id = str(contrato.contra_vistoria.id)
        else:
            contra_vistoria_id = None

        return Contratos(
            id=str(contrato._id),
            # data_inicio=datetime.strptime(contrato.dataInicio, "%d/%m/%Y"),
            data_inicio=contrato.dataInicio,
            data_fim=contrato.dataFim,
            data_cadastro=contrato.dataCadastro,
            #locatario_id='2222',
            locatario_id=str(contrato.locatario.id),
            imovel_id=str(contrato.imovel.id),
            # imovel_id='e7c3de8c-114d-4eee-a163-9306661ac7a7',
            vistoria_inicial_id=vistoria_inicial_id,
            contra_vistoria_id=contra_vistoria_id,
            esta_ativo=contrato.estaAtivo,
            #criador_id=str(contrato.criador_id)
        )
