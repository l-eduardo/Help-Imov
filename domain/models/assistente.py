
from datetime import date
from uuid import UUID
from domain.models.funcionario import Funcionario


class Assistente(Funcionario):
    def __init__(self,
                 email: str,
                 senha: str,
                 nome: str,
                 data_nascimento: date,
                 id: UUID = UUID(int=0)
                ):
        super().__init__(email=email, senha=senha, nome=nome, data_nascimento=data_nascimento, id=id)

    def __str__(self):
        return f'<id:{self.id}, nome:{self.nome}, senha:{self.senha}, data_nasc:{self.data_nascimento}, email:{self.email}>'
