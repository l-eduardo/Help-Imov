import uuid


class Imagem:
    def __init__(self,
                 width: int,
                 height: int,
                 channels: int,
                 tamanho: int,
                 content: bytes,
                 id: uuid.UUID = None):
        if id is None:
            id = uuid.uuid4()
        self.__id: uuid.UUID = id
        self.__width: int = width
        self.__height: int = height
        self.__channels: int = channels
        self.__tamanho: int = tamanho
        self.__content: bytes = content

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def channels(self) -> int:
        return self.__channels

    @property
    def tamanho(self) -> int:
        return self.__tamanho

    @property
    def content(self) -> bytes:
        return self.__content
