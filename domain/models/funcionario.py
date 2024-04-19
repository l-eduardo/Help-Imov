from datetime import date
from typing import List
from uuid import UUID
from domain.models.contrato import Contrato
from domain.models.usuario import Usuario


class Funcionario(Usuario):
    def __init__(self, email: str, senha: str, nome: str, data_nascimento: date, id: UUID = UUID(int=0)):
        super().__init__(email=email, senha=senha, nome=nome, data_nascimento=data_nascimento, id=id)
        self._contratos: List[Contrato] = []

    @property
    def contratos(self) -> 'List[Contrato]':
        return self._contratos
