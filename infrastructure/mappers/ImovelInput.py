from typing import List
from uuid import UUID

from domain.models.imovel import Imovel
from infrastructure.models.imagens import Imagens
from infrastructure.models.imoveis import Imoveis


class ImovelInputMapper:
    @staticmethod
    def map_imovel_input(imovel_from_db: Imoveis):
        imovel = Imovel(
            id=UUID(imovel_from_db.id),
            codigo=imovel_from_db.codigo,
            endereco=imovel_from_db.endereco,
            imagens=imovel_from_db.imagens
        )

        return imovel
