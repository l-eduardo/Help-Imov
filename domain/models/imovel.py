from typing import List
import uuid
from domain.models.Imagem import Imagem


class Imovel:
    def __init__(self,
                 codigo: int,
                 endereco: str,
                 imagens: List[Imagem] = None,
                 id: uuid.UUID = None):
        if id is None:
            id = uuid.uuid4()
        self._id: uuid.UUID = id
        self._codigo = codigo
        self._endereco = endereco
        self._imagens: List[Imagem] = imagens

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def endereco(self) -> str:
        return self._endereco

    @property
    def codigo(self) -> int:
        return self._codigo

    @property
    def imagens(self) -> List[Imagem]:
        return self._imagens

    @codigo.setter
    def codigo(self, codigo: int):
        self._codigo = codigo

    @endereco.setter
    def endereco(self, endereco: str):
        self._endereco = endereco

    def __str__(self):
        return f'{self.endereco}'
