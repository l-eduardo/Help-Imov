import uuid
from domain.models.usuario import Usuario


class Mensagem:
    def __init__(self, 
                 usuario: Usuario,
                 mensagem: str,
                 datetime: str,
                 id: uuid.UUID = None
                 ) -> None:
        
        if id == None:
            id = uuid.uuid4()
        self.__id = id
        self.__usuario = usuario
        self.__mensagem = mensagem
        self.__datetime = datetime

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def usuario(self) -> Usuario:
        return self.__usuario
    
    @property
    def mensagem(self) -> str:
        return self.__mensagem
    
    @property
    def datetime(self) -> str:
        return self.__datetime