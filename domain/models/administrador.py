from datetime import date
from uuid import UUID
from domain.models.funcionario import Funcionario


class Administrador(Funcionario):
    def __init__(self,
                 email: str,
                 senha: str,
                 nome: str,
                 data_nascimento: date,
                 id: UUID = UUID(int=0),
                 is_root: bool = False
                ):
        super().__init__(email=email, senha=senha, nome=nome, data_nascimento=data_nascimento, id=id)
        self._is_root: bool = is_root

    @property
    def is_root(self) -> bool:
        return self._is_root
