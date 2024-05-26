from typing import List
import uuid
from domain.models.contrato import Contrato
from datetime import date, datetime


class Vistoria:
    def __init__(self,
                 fechada: bool,
                 imagens: List[List[bytes]],
                 documento: List[bytes],
                 id: uuid.UUID = None
                 ) -> None:
        if id is None:
            id = uuid.uuid4()

        self._id = id
        self._vistoria = contra_vistoria
        self._contrato = contrato
        self._dataCadastro = datetime.strptime(f"{date.today()}", "%Y-%m-%d")
        self._anexos = anexos
        self._descricao = descricao

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def contra_vistoria(self) -> 'Vistoria':
        return self._vistoria

    @contra_vistoria.setter
    def contra_vistoria(self, value: 'Vistoria') -> None:
        self._vistoria = value

    @property
    def contrato(self) -> Contrato:
        return self._contrato

    @property
    def e_contestacao(self) -> bool:
        return self._e_contestacao

    @property
    def fechada(self) -> bool:
        return self._fechada

    @fechada.setter
    def fechada(self, value: bool) -> None:
        self._fechada = value

    @property
    def anexos(self) -> List[List[bytes]]:
        return self._anexos

    @anexos.setter
    def anexos(self, value: List[bytes]) -> None:
        self._anexos = value

    @property
    def descricao(self) -> str:
        return self._descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self._descricao = descricao

    @property
    def dataCadastro(self) -> date:
        return self._dataCadastro

    @dataCadastro.setter
    def dataCadastro(self, value: date):
        self._dataCadastro = value

    def esta_fechada(self):
        subtr_data = datetime.strptime(f"{date.today()}", "%Y-%m-%d") - self._dataCadastro
        if (subtr_data > 14):
            return False
        else:
            return True