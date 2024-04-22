
from domain.models.ocorrencia import Ocorrencia
from datetime import date
from typing import List
from uuid import UUID
from domain.models.usuario import Usuario


class PrestadorServico(Usuario):
    def __init__(self,
    nome: str,
    email: str,
    senha: str,
    especialidade: str,
    empresa: str,
    data_nascimento: date,
    id: UUID = UUID(int=0)):
        super().__init__(nome=nome, email=email, senha=senha, data_nascimento=data_nascimento, id=id)
        self._especialidade: especialidade
        self._empresa: empresa
        self._ocorrencias: List[Ocorrencia] = []

    @property
    def especialidade(self) -> str:
        return self._especialidade

    @especialidade.setter
    def especialidade(self, value: str):
        self._especialidade = value

    @property
    def empresa(self) -> str:
        return self._empresa

    @empresa.setter
    def empresa(self, value: str):
        self._empresa = value

    @property
    def ocorrencias(self) -> 'List[Ocorrencia]':
        return self._ocorrencias

