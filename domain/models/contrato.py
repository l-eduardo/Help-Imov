from typing import TYPE_CHECKING

from domain.models.imagem import Imagem
from domain.models.chat import Chat
from domain.models.documento import Documento
from domain.models.ocorrencia import Ocorrencia
from domain.models.solicitacao import Solicitacao
from domain.enums.status import Status
from domain.models.vistoria import Vistoria

if TYPE_CHECKING:
    from domain.models.imovel import Imovel
    from domain.models.vistoria import Vistoria
    from domain.models.funcionario import Funcionario
    from domain.models.locatario import Locatario
from datetime import date, datetime
from typing import List
import uuid


class Contrato:
    def __init__(self,
                 dataInicio: date,
                 locatario: 'Locatario',
                 imovel: 'Imovel',
                 estaAtivo: bool = True,
                 #criador_id: uuid.UUID = None,
                 id: uuid.UUID = None,
                 dataFim: 'date | None' = None,
                 data_cadastro: 'date'= date.today(),
                 vistoria_inicial: 'Vistoria | None' = None,
                 contra_vistoria: 'Vistoria | None' = None,
                 ):
        if id is None:
            id = uuid.uuid4()

        self._id = id
        self._dataInicio = dataInicio
        self._dataFim = dataFim
        #self._criador_id: uuid.UUID = criador_id
        self._dataCadastro = data_cadastro
        self._locatario = locatario
        self._imovel = imovel
        self._ocorrencias = []
        self._solicitacoes = []
        self._vistoria_inicial = vistoria_inicial
        self._contra_vistoria = contra_vistoria
        self._estaAtivo = estaAtivo


    '''@property
    def criador_id(self) -> uuid.UUID:
        return self._criador_id

    @criador_id.setter
    def criador_id(self, value: uuid.UUID):
        self._criador_id = value'''

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def dataInicio(self) -> date:
        return self._dataInicio

    @dataInicio.setter
    def dataInicio(self, value: date):
        self._dataInicio = value

    @property
    def dataFim(self) -> date:
        return self._dataFim

    @dataFim.setter
    def dataFim(self, value: date):
        self._dataFim = value

    @property
    def dataCadastro(self) -> date:
        return self._dataCadastro

    @dataCadastro.setter
    def dataCadastro(self, value: date):
        self._dataCadastro = value

    @property
    def locatario(self) -> 'Locatario':
        return self._locatario

    @locatario.setter
    def locatario(self, value: 'Locatario'):
        self._locatario = value

    @property
    def imovel(self) -> 'Imovel':
        return self._imovel

    @imovel.setter
    def imovel(self, value: 'Imovel'):
        self._imovel = value

    @property
    def ocorrencias(self) -> 'List[Ocorrencia]':
        return self._ocorrencias

    @property
    def solicitacoes(self) -> 'List[Solicitacao]':
        return self._solicitacoes

    @property
    def vistoria_inicial(self) -> 'Vistoria':
        return self._vistoria_inicial

    @vistoria_inicial.setter
    def vistoria_inicial(self, value: 'Vistoria'):
        self._vistoria_inicial = value

    @property
    def contra_vistoria(self) -> 'Vistoria':
        return self._contra_vistoria

    @contra_vistoria.setter
    def contra_vistoria(self, value: 'Vistoria'):
        self._contra_vistoria = value

    @property
    def estaAtivo(self) -> bool:
        return self._estaAtivo

    @estaAtivo.setter
    def estaAtivo(self, value: bool):
        self._estaAtivo = value

    def incluir_solicitacao(self,
                            titulo: str,
                            descricao: str,
                            criador_id: uuid.UUID,
                            status: Status = Status.ABERTO,
                            data_criacao: date = None,
                            id: uuid.UUID = None):
        if id is None:
            id = uuid.uuid4()
        if data_criacao is None:
            data_criacao = date.today()

        self._solicitacoes.append(Solicitacao(titulo=titulo, descricao=descricao,status=status, criador_id=criador_id, data_criacao=data_criacao, id=id))

    def incluir_ocorrencia(self,
                           titulo: str,
                           descricao: str,
                           criador_id: uuid.UUID,
                           prestador_id: uuid.UUID | None,
                           imagens: List[Imagem] = None,
                           status: Status = Status.ABERTO,
                           data_criacao: date = None,
                           chat: Chat = None,
                           id: uuid.UUID = None):

        if id is None:
            id = uuid.uuid4()
        if data_criacao is None:
            data_criacao = date.today()

        nova_ocorrencia = Ocorrencia(titulo=titulo,
                                 descricao=descricao,
                                 status=status,
                                 imagens=imagens,
                                 criador_id=criador_id,
                                 data_criacao=data_criacao,
                                 prestador_id=prestador_id,
                                 chat=chat,
                                 id=id)

        if nova_ocorrencia.e_valida():
            self._ocorrencias.append(nova_ocorrencia)
            return []

        return nova_ocorrencia.get_validation_errors()


    def incluir_vistoria(self,
                         descricao: str,
                         imagens: List[Imagem],
                         documento: Documento,
                         e_contestacao: bool,
                         data_criacao: date = date.today(),
                         id: uuid.UUID = None):

        if e_contestacao:
            self._contra_vistoria = Vistoria(descricao=descricao, imagens=imagens, documento=documento, data_criacao=data_criacao, id=id)
            return self._contra_vistoria
        else:
            self._vistoria_inicial = Vistoria(descricao=descricao, imagens=imagens, documento=documento, data_criacao=data_criacao, id=id)
            return self._vistoria_inicial

    def remover_ocorrencia(self, ocorrencia: Ocorrencia):
        self._ocorrencias.remove(ocorrencia)

    def remover_solicitacao(self, solicitacao: Solicitacao):
        self.solicitacoes.remove(solicitacao)

    def remover_vistoria(self, vistoria: Vistoria):
        if self._vistoria_inicial and self._vistoria_inicial.id == vistoria.id:
            self._vistoria_inicial = None
        elif self._contra_vistoria and self._contra_vistoria.id == vistoria.id:
            self._contra_vistoria = None
        else:
            raise ValueError("A vistoria especificada não pertence a este contrato.")

    def esta_fechada(self):
        subtr_data = datetime.strptime(f"{date.today()}", "%Y-%m-%d") - datetime.strptime(f"{self._dataCadastro}", "%Y-%m-%d")
        if subtr_data.days > 14:
            return True
        else:
            return False

