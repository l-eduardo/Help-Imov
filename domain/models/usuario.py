from abc import ABC
from datetime import date
import uuid


class Usuario(ABC):

    def __init__(self, email: str, senha: str, nome: str, data_nascimento: date, id: uuid.UUID = uuid.UUID(int=0)):
        self._id = id
        if id == uuid.UUID(int=0):
            self._id = uuid.uuid4()
        self._nome = nome
        self._email = email
        self._senha = senha
        self._data_criacao = date.today()
        self._data_nascimento = data_nascimento

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def email(self) -> str:
        return self._email

    @property
    def senha(self) -> str:
        return self._senha

    @property
    def data_criacao(self) -> date:
        return self._data_criacao

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def data_nascimento(self) -> date:
        return self._data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, value):
        self._data_nascimento = value
