from typing import List
import uuid


class Imovel:
    def __init__(self, codigo: int, endereco: str, imagens: List[List[bytes]], id: uuid.UUID = uuid.UUID(int=0)):
        self._id = id
        if id == uuid.UUID(int=0):
            self._id = uuid.uuid4()
        self._codigo = codigo
        self._endereco = endereco
        self._imagens = imagens

    @property
    def endereco(self) -> str:
        return self._endereco

    @property
    def codigo(self) -> int:
        return self._codigo

    @property
    def imagens(self) -> List[List[bytes]]:
        return self._imagens

    @codigo.setter
    def codigo(self, codigo: int) -> None:
        self._codigo = codigo

    @endereco.setter
    def endereco(self, endereco: str) -> None:
        self._endereco = endereco

    # a parte de imagens vai ser uma classe separada pra lidar com a manipulação
