from typing import List, Tuple
from uuid import UUID
from domain.models.administrador import Administrador
from domain.models.imovel import Imovel
from infrastructure.mappers.ImagemOutput import ImagemOutputMapper
from infrastructure.models.imagens import Imagens
from infrastructure.models.imoveis import Imoveis


class ImovelOutputMapper:
    @staticmethod
    def map_imovel_output(imovel_from_domain: Imovel) -> Imoveis:
        imagens = []
        for imagem in imovel_from_domain.imagens:
            imagens.append(ImagemOutputMapper.map(imagem,
                                                  imovel_id=imovel_from_domain.id))

        imovel_to_db = Imoveis()
        imovel_to_db.id = imovel_from_domain.id
        imovel_to_db.codigo = imovel_from_domain.codigo
        imovel_to_db.endereco = imovel_from_domain.endereco
        imovel_to_db.imagens = imagens

        return imovel_to_db
