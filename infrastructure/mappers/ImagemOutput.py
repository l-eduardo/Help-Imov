from sqlalchemy import UUID
from domain.models.Imagem import Imagem
from infrastructure.models.imagens import Imagens


class ImagemOutputMapper:
    @staticmethod
    def map(image_to_output: 'Imagem',
            vistoria_id: UUID | None = None,
            ocorrencia_id: UUID | None = None,
            imovel_id: UUID | None = None) -> 'Imagens':

        imagem = Imagens()
        imagem.imagem = image_to_output.content
        imagem.tamanho = image_to_output.tamanho
        imagem.height = image_to_output.height
        imagem.width = image_to_output.width
        imagem.channels = image_to_output.channels
        imagem.id_vistoria = vistoria_id
        imagem.id_ocorrencia = ocorrencia_id
        imagem.id_imovel = imovel_id
        imagem.id = image_to_output.id

        return imagem
