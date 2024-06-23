from domain.models.imagem import Imagem
from infrastructure.models.imagens import Imagens


class ImagemInputMapper:
    @staticmethod
    def map_imagem(imagem_from_db: Imagens) -> Imagem:
        imagem = Imagem(
            content=imagem_from_db.imagem,
            tamanho=imagem_from_db.tamanho,
            height=imagem_from_db.height,
            width=imagem_from_db.width,
            channels=imagem_from_db.channels,
            id=imagem_from_db.id
        )
        return imagem

    @staticmethod
    def bulk_map_imagens(imagens_from_db: list[Imagens]) -> list[Imagem]:
        if not imagens_from_db:
            return []
        return [ImagemInputMapper.map_imagem(imagem) for imagem in imagens_from_db]
