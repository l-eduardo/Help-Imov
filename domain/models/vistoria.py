from typing import List
import uuid
from domain.models.contrato import Contrato


class Vistoria:
    def __init__(self,
                 contra_vistoria: 'Vistoria',
                 contrato: Contrato,
                 e_contestacao: bool,
                 fechada: bool,
                 imagens: List[List[bytes]],
                 documento: List[bytes],
                 id: uuid.UUID = uuid.uuid4()
                 ) -> None:
        self._id = id
        self._vistoria = contra_vistoria
        self._contrato = contrato
        self._e_contestacao = e_contestacao
        self._fechada = fechada
        self._imagens = imagens
        self._documento = documento

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
    def imagens(self) -> List[List[bytes]]:
        return self._imagens

    @property
    def documento(self) -> List[bytes]:
        return self._documento
