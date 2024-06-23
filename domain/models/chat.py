from datetime import date
from typing import List
import uuid
from domain.models.mensagem import Mensagem
from domain.models.usuario import Usuario
from domain.models.imagem import Imagem
from domain.models.documento import Documento



class Chat:
    def __init__(self,
                 id: uuid.UUID = None,
                 mensagens: List[Mensagem] = [],
                 imagens: List[Imagem] = []):
        if id == None:
          id = uuid.uuid4()
        self._id = id
        self._mensagens = mensagens
        self._imagens = imagens

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def mensagens(self) -> List[Mensagem]:
        return self._mensagens

    @property
    def imagens(self) -> List[Imagem]:
        return self._imagens

    def incluir_mensagens(self, novas_mensagens: List[dict]):
        mensagens_instanciadas = [Mensagem(usuario=mensagem['usuario'],
                                           mensagem=mensagem['mensagem'],
                                           datetime=mensagem['datetime']) for mensagem in novas_mensagens]
        [self._mensagens.append(mensagem) for mensagem in mensagens_instanciadas]
        return mensagens_instanciadas

    def incluir_imagem(self, novas_imagens: List[Imagem]):
        for imagem in novas_imagens:
            self._imagens.append(imagem)
