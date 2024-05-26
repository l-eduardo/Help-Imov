import imageio.v3 as iio
import numpy as np

from application.controllers.session_controller import SessionController
from domain.models.session import Session
import os


class ImagensService:
    @staticmethod
    def read(dir: str) -> bytes:
        imagem = iio.imread(dir)
        imagem_bytes = imagem.tobytes()
        return imagem_bytes

    @staticmethod
    @SessionController.inject_session_data
    def local_temp_save(image_bytes: bytes, width: int, height: int, channel: int = 4, session: Session=None) -> str:
        np_image = np.frombuffer(image_bytes, dtype=np.uint8)

        reshaped_image = np_image.reshape((height, width, channel))

        iio.imwrite('temp_image.png' + session.session_id.__str__() + '.png', image=reshaped_image)

    @staticmethod
    def flush_temp_images(dir: str) -> None:
        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)

            if os.path.isfile(file_path):
                os.remove(file_path)
