from uuid import UUID

from sqlalchemy.orm import joinedload

from infrastructure.configs.connection import Connection
from infrastructure.models.contratos import Contratos
from infrastructure.mappers.ContratoInput import ContratoInputMapper
from infrastructure.models.imoveis import Imoveis
from infrastructure.models.locatarios import Locatarios
from infrastructure.models.ocorrencias import Ocorrencias
from infrastructure.models.solicitacoes import Solicitacoes


from infrastructure.models.ocorrencias import Ocorrencias

class ContratosRepositories:
    def get_all(self) -> list[Contratos]:
        with Connection() as connection:
            result = connection.session.query(Contratos).all()
            result_mapped = [ContratoInputMapper.map_contrato(x) for x in result]

            return result_mapped

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

    def update(self, contrato: Contratos) -> Contratos:
        if contrato.vistoria_inicial is not None:
            vistoria_inicial_id = str(contrato.vistoria_inicial.id)
        else:
            vistoria_inicial_id = None
        
        if contrato.contra_vistoria is not None:
            contra_vistoria_id = str(contrato.contra_vistoria.id)
        else:
            contra_vistoria_id = None

        with Connection() as connection:
            result = connection.session.query(Contratos).filter(Contratos.id == str(contrato.id)).update(
                {"contra_vistoria_id": contra_vistoria_id,
                 "vistoria_inicial_id": vistoria_inicial_id})
            connection.session.commit()
            return contrato


