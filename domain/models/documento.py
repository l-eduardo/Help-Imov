import uuid


class Documento:
    def __init__(self,
                 tipo: str,
                 content: bytes,
                 id: uuid.UUID = None):
        if id is None:
            id = uuid.uuid4()
        self.__id: uuid.UUID = id
        self.__tipo: str = tipo
        self.__content: bytes = content

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def tipo(self) -> str:
        return self.__tipo

    @property
    def content(self) -> bytes:
        return self.__content
