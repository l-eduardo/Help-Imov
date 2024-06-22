import time
from typing import List, Tuple
import uuid
import imageio.v3 as iio
import numpy as np

from application.controllers.session_controller import SessionController
from domain.models.Imagem import Imagem
from domain.models.session import Session
import os


class ImagensService:
    @staticmethod
    def read(dir: str) -> Imagem:
        imagem_shape = iio.imread(dir)
        imagem_bytes = imagem_shape.tobytes()

        return Imagem(height=imagem_shape.shape[0],
                      width=imagem_shape.shape[1],
                      channels=imagem_shape.shape[2],
                      tamanho=imagem_shape.size,
                      content=imagem_bytes)

    @staticmethod
    def bulk_read(dir_list: List[str]) -> List[Imagem]:
        return [ImagensService.read(image) for image in dir_list]

    @staticmethod
    @SessionController.inject_session_data
    def local_temp_save(imagem: Imagem,
                        session: Session = None) -> str:

        if imagem is None:
            return None

        np_image = np.frombuffer(imagem.imagem if hasattr(imagem, 'imagem') else imagem.content, dtype=np.uint8)
        reshaped_image = np_image.reshape((imagem.height, imagem.width, imagem.channels))

        # Defina o caminho do diretório temporário
        temp_dir = './tmp'

        # Verifique se o diretório existe, caso contrário, crie-o
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        salt = time.time_ns()
        path = os.path.join(temp_dir, f"{session.session_id}_temp_image_{salt}.png")
        iio.imwrite(path, image=reshaped_image)
        return path

    @staticmethod
    def bulk_local_temp_save(imagens: List[Imagem]) -> List[str]:
        if not imagens or imagens is None:
            return []
        return [ImagensService.local_temp_save(imagem) for imagem in imagens]

    @staticmethod
    @SessionController.inject_session_data
    def flush_temp_images(session: Session = None) -> None:
        session_id = session.session_id.__str__()
        temp_dir = './tmp'

        if os.path.exists(temp_dir):
            for filename in os.listdir(temp_dir):
                if filename.startswith(session_id):
                    file_path = os.path.join(temp_dir, filename)

                    if os.path.isfile(file_path):
                        os.remove(file_path)
