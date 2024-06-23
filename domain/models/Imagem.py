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
        self.imagem = None
        self.__id: uuid.UUID = id
        self.__width: int = width
        self.__height: int = height
        self.__channels: int = channels
        self.__tamanho: int = tamanho
        self.__content: bytes = content

    def e_valida(self) -> bool:
        return self.__width_e_valido() and \
               self.__height_e_valido() and \
               self.__channels_e_valido() and \
               self.__content_e_valido()

    def __content_e_valido(self) -> bool:
        return self.__content is not None

    def __height_e_valido(self) -> bool:
        return self.__height >= 720 and self.__height <= 1280

    def __width_e_valido(self) -> bool:
        return self.__width >= 1280 and self.__width <= 1920

    def __channels_e_valido(self) -> bool:
        return self.__channels > 0

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
