from domain.models.vistoria import Vistoria
from infrastructure.models.vistorias import Vistorias


class VistoriasOutputMapper:

    # iimplementar depois com os anexos
    @staticmethod
    def map_vistoria(vistoria: Vistoria) -> Vistorias:
        return Vistorias(
            id=vistoria._id,
            anexos=vistoria._anexos,
            contrato=vistoria.contrato,
            data_criacao=vistoria.dataCadastro,
            descricao=vistoria.descricao,
            econtestacao=vistoria.e_contestacao,
            estaFechada=vistoria.fechada
        )
