from uuid import UUID
from domain.models.imovel import Imovel
from infrastructure.configs.connection import Connection
from infrastructure.mappers.ImovelInput import ImovelInputMapper
from infrastructure.mappers.ImovelOutput import ImovelOutputMapper
from infrastructure.models import imagens
from infrastructure.models.imagens import Imagens
from infrastructure.models.imoveis import Imoveis


class ImoveisRepository:
    def get_all_with_images(self) -> list[Imovel]:
        with Connection() as connection:
            result = connection.session.query(Imoveis, Imagens).filter(Imoveis.id == Imagens.id) \
                .all()

            #connection.session.query(Imoveis, Imagens).filter(Imoveis.id == Imagens.id) \
            imovel_inputs_list = []
            for i in result:
                imovel_inputs_list.append(ImovelInputMapper.map_imovel_input(i[0], i[1]))

            return imovel_inputs_list

    def get_all(self) -> list[Imovel]:
         with Connection() as connection:
            result = connection.session.query(Imoveis).all()
            return [ImovelInputMapper.map_imovel_input(x) for x in result]

    def get_by_id_with_images(self, id: UUID) -> Imoveis:
        with Connection() as connection:
            return connection.session.query(Imoveis)\
                .filter(Imoveis.id == id)\
                .join(Imagens, Imoveis.id == Imagens.id)\
                .first()

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            result = connection.session.query(Imoveis).filter(Imoveis.id == str(id)).delete()
            connection.session.commit()

    def insert(self, imovel: Imoveis) -> Imoveis:
        imovel_to_db = ImovelOutputMapper.map_imovel_output(imovel_from_domain=imovel)

        with Connection() as connection:
            connection.session.add(imovel_to_db)
            connection.session.commit()
            return imovel

    def update(self, imovel: Imoveis) -> Imoveis:
        with Connection() as connection:
            result = connection.session.query(Imoveis).filter(Imoveis.id == str(imovel.id)).update(
                {"codigo": imovel.codigo,
                 "endereco": imovel.endereco,
                 "imagens": imovel.imagens}

            )

            connection.session.commit()
            return imovel

    def get_by_id(self, id: UUID) -> Imovel:
        with Connection() as connection:
            return connection.session.query(Imovel)\
                .filter(Imovel.id == id)\
                .first()
