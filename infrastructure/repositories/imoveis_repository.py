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
                print(i)

            return imovel_inputs_list

    def get_by_id_with_images(self, id: UUID) -> Imoveis:
        with Connection() as connection:
            return connection.session.query(Imoveis)\
                .filter(Imoveis.id == id)\
                .join(Imagens, Imoveis.id == Imagens.id)\
                .first()

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            connection.session.query(Imagens).filter(Imagens.id == id).delete()
            connection.session.query(Imoveis).filter(Imoveis.id == id).delete()

    def insert(self, imovel: Imovel) -> Imoveis:
        with Connection() as connection:
            imovel_output = ImovelOutputMapper.map_imovel_output(imovel)
            connection.session.add(imovel_output[0])
            connection.session.add(imovel_output[1])

            return imovel_output[0]

    def get_by_id(self, id: UUID) -> Imovel:
        with Connection() as connection:
            return connection.session.query(Imovel)\
                .filter(Imovel.id == id)\
                .first()
