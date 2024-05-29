from typing import TYPE_CHECKING, List
import uuid
from domain.models.Imagem import Imagem
from domain.models.documento import Documento
if TYPE_CHECKING:
    from domain.models.contrato import Contrato
from datetime import date, datetime


class Vistoria:
    def __init__(self,
                 imagens: List[Imagem],
                 descricao: str,
                 documento: Documento,
                 fechada: bool = False,
                 data_cadastro: 'date' = date.today(),
                 id: uuid.UUID = None):
        if id is None:
            id = uuid.uuid4()

        self._id: uuid.UUID = id
        self._descricao = descricao
        self._data_criacao = data_cadastro
        self._imagens = imagens
        self._documento = documento
        print(data_cadastro)

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def documento(self) -> Documento:
        return self._documento

    @documento.setter
    def documento(self, value: List[bytes]) -> None:
        self._documento = value

    @property
    def imagens(self) -> List[Imagem]:
        return self._imagens

    @imagens.setter
    def imagens(self, value: List[Imagem]) -> None:
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
        print(subtr_data)
        print(date.today())
        print(self._data_criacao)
        if subtr_data.days > 14:
            return True
        else:
            return False
