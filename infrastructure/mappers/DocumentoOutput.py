from sqlalchemy import UUID
from domain.models.documento import Documento
from infrastructure.models.documentos import Documentos


class DocumentoOutputMapper:
    @staticmethod
    #TODO VERIFICAR SE VAI DAR PAU
    def map(documento: Documento, vistoria_id: UUID | None, chat_id: UUID = None) -> Documentos:
        documento_to_db = Documentos()

        documento_to_db.id = documento.id
        documento_to_db.documento = documento.content
        documento_to_db.tipo = documento.tipo
        documento_to_db.vistoria_id = vistoria_id
        documento_to_db.id_chat = chat_id

        return documento_to_db
