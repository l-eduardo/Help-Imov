from uuid import UUID
from infrastructure.configs.connection import Connection
from infrastructure.models.imagens import Imagens
from infrastructure.models.imoveis import Imoveis


class ImoveisRepository:
    def get_all_with_images(self) -> list[Imoveis]:
        with Connection() as connection:
            return connection.session.query(Imoveis)\
                .join(Imagens, Imoveis.id == Imagens.id)\
                .all()

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

    def insert(self, imovel) -> Imoveis:
        with Connection() as connection:
            connection.session.add(imovel)
            return imovel
