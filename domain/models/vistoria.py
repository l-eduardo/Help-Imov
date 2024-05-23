from typing import List
import uuid
from domain.models.contrato import Contrato
from datetime import date


class Vistoria:
    def __init__(self,
                 contra_vistoria: 'Vistoria',
                 contrato: Contrato,
                 e_contestacao: bool,
                 fechada: bool,
                 anexos: List[List[bytes]],
                 descricao: str,
                 id: uuid.UUID = uuid.uuid4()
                 ):
        self._id = id
        self._vistoria = contra_vistoria
        self._contrato = contrato
        self._dataCadastro = date.today()
        self._e_contestacao = e_contestacao
        self._fechada = fechada
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
