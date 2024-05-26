from typing import List
from uuid import UUID
from sqlalchemy import create_engine, Table, MetaData, select, delete, insert
from sqlalchemy.orm import sessionmaker

from infrastructure.configs.connection import Connection
from infrastructure.models.imagens import Imagens

class ImagensRepository:
    def get_imagem_by_id(self, id: UUID) -> Imagens:
        with Connection() as connection:
            result = connection.session.query(Imagens).filter(Imagens.id == str(id)).first()

        return result

    def save_imagem(self, imagem: Imagens):
        with Connection() as connection:
            connection.session.add(imagem)
            connection.session.commit()

    def delete_imagem(self, imagem_id):
        query = delete(self.imagens).where(self.imagens.c.id == imagem_id)
        self.session.execute(query)
        self.session.commit()
