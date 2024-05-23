from uuid import UUID

from sqlalchemy.orm import joinedload

from infrastructure.configs.connection import Connection
from infrastructure.models.contratos import Contratos
from infrastructure.models.imoveis import Imoveis
from infrastructure.models.locatarios import Locatarios
from infrastructure.models.ocorrencias import Ocorrencias
from infrastructure.models.solicitacoes import Solicitacoes


class ContratosRepositories:
    def get_all(self) -> list[Contratos]:
        with Connection() as connection:
            self.get_todos_contratos_completos()
            return connection.session.query(Contratos).all()


    def get_todos_contratos_completos(self):
        with Connection() as connection:
            '''resultado = connection.session.query(Contratos, Solicitacoes, Ocorrencias, Locatarios, Imoveis)\
            .join(Solicitacoes, Contratos.id == Solicitacoes.id_contrato, isouter=False)\
            .join(Ocorrencias, Contratos.id == Ocorrencias.id_contrato, isouter=True)\
            .join(Locatarios, Contratos.locatario_id == Locatarios.id, isouter=True)\
            .join(Imoveis, Contratos.imovel_id == Imoveis.id, isouter=True).all()'''

            resultado = connection.session.query(Contratos).options(
                joinedload(Contratos.locatario_id),
                joinedload(Contratos.solicitacoes),
                joinedload(Contratos.ocorrencias),
                joinedload(Contratos.imovel_id)
            ).all()
            print(resultado)


    def get_by_id(self, id: UUID) -> Contratos:
        with Connection() as connection:
            return connection.session.query(Contratos)\
                .filter(Contratos.id == id)\
                .first()

    def get_by_locatario_id(self, locatario_id: UUID) -> list[Contratos]:
        with Connection() as connection:
            return connection.session.query(Contratos)\
                .filter(Contratos.locatario_id == locatario_id)\
                .all()

    def insert(self, contrato: Contratos) -> Contratos:
        with Connection() as connection:
            connection.session.add(contrato)
            connection.session.commit()
            return contrato


