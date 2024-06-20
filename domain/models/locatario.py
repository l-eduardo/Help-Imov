from datetime import date
from typing import List
from uuid import UUID
from domain.models.contrato import Contrato
from domain.models.usuario import Usuario


class Locatario(Usuario):
    def __init__(self, email: str, senha: str, nome: str, data_nascimento: date, id: UUID = UUID(int=0), celular: str = ''):
        super().__init__(email=email, senha=senha, nome=nome, data_nascimento=data_nascimento, id=id)

        #self._contratos: List[Contrato] = []
        self._celular: str = celular

    @property
    def celular(self) -> str:
        return self._celular

    @celular.setter
    def celular(self, celular) -> str:
        self._celular = celular

    def __str__(self):
        return f'{self.id},{self.nome},{self.senha},{self.data_nascimento},{self.email},{self.celular}'
