from datetime import date
from typing import List
import uuid
from domain.models.mensagem import Mensagem
from domain.models.usuario import Usuario


class Chat:
    def __init__(self,
                 id: uuid.UUID = None, 
                 mensagens: List[Mensagem] = []):
        if id == None:
          id = uuid.uuid4()
        self._id = id
        self._mensagens = mensagens

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def mensagens(self) -> List[Mensagem]:
        return self._mensagens

    def incluir_mensagens(self, novas_mensagens: List[dict]):
        mensagens_instanciadas = [Mensagem(usuario=mensagem['usuario'],
                                           mensagem=mensagem['mensagem'],
                                           datetime=mensagem['datetime']) for mensagem in novas_mensagens]
        [self._mensagens.append(mensagem) for mensagem in mensagens_instanciadas]
        return mensagens_instanciadas
