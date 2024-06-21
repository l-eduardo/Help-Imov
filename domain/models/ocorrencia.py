from datetime import date
from typing import List
import uuid
from typing import TYPE_CHECKING
from domain.enums.status import Status
from domain.models.Imagem import Imagem
from domain.models.chat import Chat
if TYPE_CHECKING:
    from domain.models.prestador_servico import PrestadorServico


class Ocorrencia:
    def __init__(self,
    titulo: str,
    descricao: str,
    criador_id: uuid.UUID,
    imagens: List[Imagem] = None,
    status: Status = Status.ABERTO,
    data_criacao: date = None,
    id: uuid.UUID = None):

        if id is None:
            id = uuid.uuid4()
        if data_criacao is None:
            data_criacao = date.today()

        self._imagens: List[Imagem] = imagens
        self._id: uuid.UUID = id
        self._titulo: str = titulo
        self._descricao: str = descricao
        self._status: Status = status
        self._data_criacao: date = data_criacao
        self._criador_id: uuid.UUID = criador_id
        self._prestadores_servico: List[PrestadorServico] = []

    @property
    def criador_id(self) -> uuid.UUID:
        return self._criador_id

    @criador_id.setter
    def criador_id(self, value: uuid.UUID):
        self._criador_id = value

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

    @property
    def prestador_servico(self) -> 'List[PrestadorServico]':
        return self._prestadores_servico

    @property
    def imagens(self) -> List[Imagem]:
        return self._imagens

    def incluir_chat(self, participantes):
        return Chat(participantes = participantes, id = uuid.uuid4())