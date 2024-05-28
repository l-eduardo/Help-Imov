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

    def e_valida(self) -> bool:
        return self.__width_e_valido(self.width) and \
               self.__height_e_valido(self.height) and \
               self.__channels_e_valido(self.channels) and \
               self.__content_e_valido(self.tamanho)

    def __content_e_valido(self, content: bytes) -> bool:
        return content is not None

    def __height_e_valido(self, height: int) -> bool:
        return height >= 720 and height <= 1280

    def __width_e_valido(self, width: int) -> bool:
        return width >= 1280 and width <= 1920

    def __channels_e_valido(self, channels: int) -> bool:
        return channels > 0

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
