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
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def endereco(self) -> str:
        return self._endereco

    @property
    def codigo(self) -> int:
        return self._codigo

    @property
    def imagens(self) -> List[List[bytes]]:
        return self._imagens
