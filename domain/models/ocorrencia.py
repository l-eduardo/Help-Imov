from datetime import date
from typing import List
import uuid
from typing import TYPE_CHECKING
from domain.enums.status import Status
from domain.models.Imagem import Imagem
from domain.models.chat import Chat
from domain.models.domain_model import DomainModel
if TYPE_CHECKING:
    from domain.models.prestador_servico import PrestadorServico


class Ocorrencia(DomainModel):
    def __init__(self,
                 titulo: str,
                 descricao: str,
                 criador_id: uuid.UUID,
                 prestador_id: uuid.UUID = None,
                 imagens: List[Imagem] = None,
                 status: Status = Status.ABERTO,
                 data_criacao: date = None,
                 id: uuid.UUID = None,
                 chat: Chat = None):
        super().__init__()

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
        self._prestador_id: uuid.UUID = prestador_id
        self._chat: Chat = chat

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
    def prestador_id(self) -> uuid.UUID:
        return self._prestador_id

    @prestador_id.setter
    def prestador_id(self, value: uuid.UUID):
        self._prestador_id = value

    @property
    def imagens(self) -> List[Imagem]:
        return self._imagens

    @property
    def chat(self) -> Chat:
        return self._chat


    def incluir_chat(self):
        return Chat()

    def e_valida(self) -> bool:
        if not self.__titulo_e_valido():
            self.add_validation_error('Título é obrigatório')
        if not self.__descricao_e_valido():
            self.add_validation_error('Descrição é obrigatória')
        if not self.__status_e_valido():
            self.add_validation_error('Status é obrigatório')
        if not self.__data_criacao_e_valido():
            self.add_validation_error('Data de criação é obrigatória e deve ser anterior a data atual')
        if not self.__criador_id_e_valido():
            self.add_validation_error('Criador é obrigatório')
        if not self.__imagens_sao_validas():
            self.add_validation_error('Imagens inválidas. Por favor, selecione somente imagens com resolucao entre 1280x720 e 1820x1280 pixels!')

        return len(self.get_validation_errors()) == 0


    def __titulo_e_valido(self) -> bool:
        return self._titulo is not None and len(self._titulo) > 0

    def __descricao_e_valido(self) -> bool:
        return self._descricao is not None and len(self._descricao) > 0

    def __status_e_valido(self) -> bool:
        return self._status is not None

    def __data_criacao_e_valido(self) -> bool:
        return self._data_criacao is not None and self._data_criacao <= date.today()

    def __criador_id_e_valido(self) -> bool:
        return self._criador_id is not None

    def __imagens_sao_validas(self) -> bool:
        return self._imagens is not None and all([imagem.e_valida() for imagem in self._imagens])
