from typing import List
from uuid import UUID

from domain.models.imovel import Imovel
from infrastructure.models.imagens import Imagens
from infrastructure.models.imoveis import Imoveis


class ImovelInputMapper:

    @staticmethod
    def map_imovel_input(imovel: Imoveis) -> Imovel:
        return Imovel(
            id=UUID(imovel.id),
            endereco=imovel.endereco,
            codigo=imovel.codigo,
            imagens=imovel.imagens
        )