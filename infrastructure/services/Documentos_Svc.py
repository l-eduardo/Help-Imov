import os
import time
import magic
from application.controllers.session_controller import SessionController
from domain.models.documento import Documento
from domain.models.session import Session


class DocumentosService:
    __save_dir = './downloads'

    @staticmethod
    def read_file(dir: str) -> 'Documento':
        with open(dir, 'rb') as file:
            file_bytes = file.read()

        tipo = magic.from_buffer(file_bytes).split(',')[0]

        documento = Documento(
            content = file_bytes,
            tipo=tipo)

        return documento

    @staticmethod
    @SessionController.inject_session_data
    def save_file(documento: Documento, session: Session = None) -> None:
        if not os.path.exists(DocumentosService.__save_dir):
            os.makedirs(DocumentosService.__save_dir)
        salt = time.time_ns()
        document_path = f"{DocumentosService.__save_dir}/{salt.__str__()}_{documento.id.__str__()}.{documento.tipo.split(' ')[0].lower()}"
        print(document_path)
        with open(document_path, 'wb') as file:
            file.write(documento.content)
        return document_path
