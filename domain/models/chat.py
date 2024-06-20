from datetime import date
from typing import List
import uuid

from domain.models.usuario import Usuario


class Chat:
    def __init__(self, participantes: List[Usuario],
                 messages: List[tuple[uuid.UUID, str, date]],
                 id: uuid.UUID = uuid.UUID(int=0)):
        self._id = id
        self._participantes = participantes
        self._mensagens = messages

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def participantes(self) -> List[Usuario]:
        return self._participantes

    @property
    def mensagens(self) -> List[tuple[uuid.UUID, str, date]]:
        return self._mensagens
