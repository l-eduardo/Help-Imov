import uuid
from uuid import UUID
from domain.models.vistoria import Vistoria
from infrastructure.configs.connection import Connection
from infrastructure.mappers.VistoriasOutput import VistoriasOutputMapper
from infrastructure.models.vistorias import Vistorias


class VistoriasRepository:
    def get_all(self) -> list[Vistorias]:
        with Connection() as connection:
            return connection.session.query(Vistorias).all()

    def get_by_id(self, id: UUID) -> Vistorias:
        with Connection() as connection:
            return connection.session.query(Vistorias) \
                .filter(Vistorias.id == id) \
                .first()


    def insert(self, vistoria: Vistorias) -> Vistorias:
        vistoria_to_db = VistoriasOutputMapper.map_vistoria(vistoria_from_domain=vistoria)

        with Connection() as connection:
            connection.session.add(vistoria_to_db)
            connection.session.commit()
            return vistoria

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            result = connection.session.query(Vistorias).filter(Vistorias.id == str(id)).delete()
            connection.session.commit()

    def update(self, vistoria: Vistorias) -> Vistorias:
        with Connection() as connection:
            result = connection.session.query(Vistorias).filter(Vistorias.id == str(vistoria.id)).update(
                {"descricao": vistoria.descricao})
                 # "imagens": vistoria.imagens,
                 # "documentos": vistoria.documento})
            connection.session.commit()
            return vistoria

    def get_vistoria_inicial_by_contrato_id(self, contrato_id: UUID) -> Vistorias:
        with Connection() as connection:
            return connection.session.query(Vistorias) \
                .filter(Vistorias.contrato_id == contrato_id) \
                .filter(Vistorias.tipo == 'inicial') \
                .first()

    def get_contra_vistoria_by_contrato_id(self, contrato_id: UUID) -> Vistorias:
        with Connection() as connection:
            return connection.session.query(Vistorias) \
                .filter(Vistorias.contrato_id == contrato_id) \
                .filter(Vistorias.tipo == 'contra') \
                .first()


