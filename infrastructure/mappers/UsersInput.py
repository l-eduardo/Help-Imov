from typing import List
from uuid import UUID

from domain.models.locatario import Locatario
from infrastructure.models.imagens import Imagens
from infrastructure.models.locatarios import Locatarios


class UsersInputMapper:
    @staticmethod
    def map_locatario_input(locatario_from_db: Locatarios):
        locatario = Locatarios(
            id=UUID(locatario_from_db.id),
            nome=locatario_from_db.nome,
            data_nascimento=locatario_from_db.data_nascimento,
            #email=locatario_from_db.email,
            #senha=locatario_from_db.senha,
        )
        return locatario
