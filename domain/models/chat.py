from typing import List
import uuid
from domain.models.mensagem import Mensagem
from domain.models.imagem import Imagem
from domain.models.documento import Documento


class Chat:
    def __init__(self,
                 id: uuid.UUID = None,
                 mensagens: List[Mensagem] = [],
                 documentos: List[Documento] = [],
                 imagens: List[Imagem] = []):
        if id == None:
          id = uuid.uuid4()
        self.__id = id
        self.__mensagens = mensagens
        self.__documentos = documentos
        self.__imagens = imagens

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def mensagens(self) -> List[Mensagem]:
        return self.__mensagens
    
    @property
    def documentos(self) -> List[Documento]:
        return self.__documentos

    @property
    def imagens(self) -> List[Imagem]:
        return self.__imagens

    def incluir_mensagens(self, novas_mensagens: List[dict]):
        mensagens_instanciadas = [Mensagem(usuario=mensagem['usuario'],
                                           mensagem=mensagem['mensagem'],
                                           datetime=mensagem['datetime']) for mensagem in novas_mensagens]
        [self.__mensagens.append(mensagem) for mensagem in mensagens_instanciadas]
        return mensagens_instanciadas

    def incluir_imagens(self, novas_imagens: List[Imagem]):
        for imagem in novas_imagens:
            self.__imagens.append(imagem)

    def incluir_documentos(self, novos_documentos: List[Documento]):
        for documento in novos_documentos:
            self.__imagens.append(documento)
