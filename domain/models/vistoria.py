from typing import List
import uuid
from datetime import date, datetime


class Vistoria:
    def __init__(self,
                 descricao: str,
                 imagens: List[List[bytes]],
                 documento: List[bytes],
                 id: uuid.UUID = None):
        if id is None:
            id = uuid.uuid4()

        self._id: uuid.UUID = id
        self._descricao = descricao
        self._data_criacao = date.today()
        self._imagens = imagens
        self._documento = documento


    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def documento(self) -> List[bytes]:
        return self._documento

    @documento.setter
    def documento(self, value: List[bytes]) -> None:
        self._documento = value

    @property
    def imagens(self) -> List[List[bytes]]:
        return self._imagens

    @imagens.setter
    def imagens(self, value: List[List[bytes]]) -> None:
        self._imagens = value

    @property
    def descricao(self) -> str:
        return self._descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self._descricao = descricao

    @property
    def data_criacao(self) -> date:
        return self._data_criacao

    @data_criacao.setter
    def data_criacao(self, value: date):
        self._data_criacao = value

    def esta_fechada(self):
        subtr_data = datetime.strptime(f"{date.today()}", "%Y-%m-%d") - datetime.strptime(f"{self._data_criacao}", "%Y-%m-%d")
        if (subtr_data > 14):
            return False
        else:
            return True
