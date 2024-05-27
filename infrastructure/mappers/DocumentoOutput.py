from sqlalchemy import UUID
from domain.models.documento import Documento
from infrastructure.models.documentos import Documentos


class DocumentoOutputMapper:
    @staticmethod
    def map(documento: Documento, vistoria_id: UUID) -> Documentos:
        documento_to_db = Documentos()

        documento_to_db.id = documento.id
        documento_to_db.documento = documento.content
        documento_to_db.tipo = documento.tipo
        documento_to_db.vistoria_id = vistoria_id

        return documento_to_db
