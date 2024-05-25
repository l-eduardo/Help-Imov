from datetime import date
import uuid

from domain.enums.status import Status


class Solicitacao:
    def __init__(self,
     titulo: str,
     descricao: str,
     status: Status = Status.ABERTO,
     data_criacao: date = None,
     id: uuid.UUID = None):
        if id is None:
            id = uuid.uuid4()
        if data_criacao is None:
            data_criacao = date.today()

        self._id: uuid.UUID = id
        self._titulo: str = titulo
        self._descricao: str = descricao
        self._status: Status = status
        self._data_criacao: date = data_criacao

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, value: str):
        self._titulo = value

    @property
    def descricao(self) -> str:
        return self._descricao

    @descricao.setter
    def descricao(self, value: str):
        self._descricao = value

    @property
    def status(self) -> Status:
        return self._status

    @status.setter
    def status(self, value: Status):
        self._status = value

    @property
    def data_criacao(self) -> date:
        return self._data_criacao

