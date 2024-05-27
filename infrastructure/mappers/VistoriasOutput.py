from uuid import UUID
from domain.models.vistoria import Vistoria
from infrastructure.mappers.ImagemOutput import ImagemOutputMapper
from infrastructure.models.vistorias import Vistorias


class VistoriasOutputMapper:

    @staticmethod
    def map_vistoria(vistoria_from_domain: Vistoria, id_contrato: UUID) -> Vistorias:
        imagens = []
        for imagem in vistoria_from_domain.imagens:
            imagens.append(ImagemOutputMapper.map(imagem,
                                                  vistoria_id=vistoria_from_domain.id))

        vistoria_to_db = Vistorias()
        vistoria_to_db.id = vistoria_from_domain.id
        vistoria_to_db.descricao = vistoria_from_domain.descricao
        vistoria_to_db.data_criacao = vistoria_from_domain.data_criacao
        vistoria_to_db.documento = vistoria_from_domain.documento
        vistoria_to_db.imagens = imagens
        vistoria_to_db.id_contrato = id_contrato


        return vistoria_to_db
