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
                 e_root: bool = False
                ):
        super().__init__(email=email, senha=senha, nome=nome, data_nascimento=data_nascimento, id=id)
        self._e_root: bool = e_root

    @property
    def e_root(self) -> bool:
        return self._e_root

    def __str__(self):
        return f'{self.id},{self.nome},{self.senha},{self.data_nascimento},{self.email},{self.e_root}'