from typing import List
import uuid

from domain.models.Imagem import Imagem


class Imovel:
    def __init__(self,
                 codigo: int,
                 endereco: str,
                 imagens: List[Imagem],
                 id: uuid.UUID = uuid.UUID(int=0)):
        self._id = id
        if id == uuid.UUID(int=0):
            self._id = uuid.uuid4()
        self._codigo = codigo
        self._endereco = endereco
        self._imagens = imagens

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
    def codigo(self, codigo: int) -> None:
        self._codigo = codigo

    @endereco.setter
    def endereco(self, endereco: str) -> None:
        self._endereco = endereco

    # a parte de imagens vai ser uma classe separada pra lidar com a manipulação

    def __str__(self):
        return f'{self.endereco}'
