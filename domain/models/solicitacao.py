from datetime import date
import uuid

from domain.enums.ocorrencia_status import Status
from domain.enums.prioridade_solicitacao import Prioridade
from domain.models.contrato import Contrato


class Solicitacao:
    def __init__(self,
                 titulo: str,
                 descricao: str,
                 contrato: Contrato,
                 status: Status = Status.ABERTO,
                 prioridade: Prioridade = Prioridade.BAIXA,
                 id: uuid.UUID = uuid.uuid4()):
        self._id: uuid.UUID = id
        self._titulo: str = titulo
        self._descricao: str = descricao
        self._status: Status = status
        self._prioridade: Prioridade = prioridade
        self._data_criacao: date = date.today()
        self._contrato: Contrato = contrato

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
    def prioridade(self) -> Prioridade:
        return self._prioridade

    @prioridade.setter
    def prioridade(self, value: Prioridade):
        self._prioridade = value

    @property
    def data_criacao(self) -> date:
        return self._data_criacao

    @property
    def contrato(self) -> 'Contrato':
        return self._contrato
