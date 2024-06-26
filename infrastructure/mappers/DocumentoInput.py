from uuid import UUID
from domain.models.documento import Documento
from infrastructure.models.documentos import Documentos


class DocumentoInputMapper:
    @staticmethod
    def map_documento(documento_from_db: Documentos) -> Documento | None:
        if documento_from_db is None:
            return None

        documento = Documento(
            content=documento_from_db.documento,
            tipo=documento_from_db.tipo,
            id=UUID(documento_from_db.id)
        )

        return documento

    @staticmethod
    def bulk_map_documento(documentos_from_db: list[Documentos]) -> list[Documento]:
        if not documentos_from_db:
            return []
        return [DocumentoInputMapper.map_documento(documento) for documento in documentos_from_db]
