from typing import List, Tuple
from domain.models.administrador import Administrador
from domain.models.imovel import Imovel
from infrastructure.models.imagens import Imagens
from infrastructure.models.imoveis import Imoveis


class ImovelOutputMapper:
    @staticmethod
    def map_administrador(imovel: Imovel) -> Tuple[Imoveis, List[Imagens]]:
        image_lista = []
        for image in imovel.imagens:
            image_lista.append(Imagens(
                id=imovel.id,
                imagem=image,
            ))

        return (Imoveis(
            id=imovel.id,
            endereco=imovel.endereco,
            codigo=imovel.codigo
        ), image_lista)
