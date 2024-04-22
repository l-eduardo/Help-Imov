from datetime import date
from typing import List
import uuid

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from domain.models.funcionario import Funcionario
    from domain.models.imovel import Imovel
    from domain.models.locatario import Locatario
    from domain.models.ocorrencia import Ocorrencia
    from domain.models.solicitacao import Solicitacao
    from domain.models.vistoria import Vistoria


class Contrato:
    def __init__(self,
    dataInicio: date,
    dataFim: date,
    locatario: 'Locatario',
    imovel: 'Imovel',
    criador: 'Funcionario',
    vistoria_inicial: 'Vistoria',
    estaAtivo: bool,
    id: uuid.UUID = uuid.uuid4()
    ):
        self._id = id
        self._dataInicio = dataInicio
        self._dataFim = dataFim
        self._dataCadastro = date.today()
        self._locatario = locatario
        self._imovel = imovel
        self._criador = criador
        self._ocorrencias = []
        self._solicitacoes = []
        self._vistoria_inicial = vistoria_inicial
        self._vistoria_final = None
        self._estaAtivo = estaAtivo

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
    def criador(self) -> 'Funcionario':
        return self._criador

    @criador.setter
    def criador(self, value: 'Funcionario'):
        self._criador = value

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
    def vistoria_final(self) -> 'Vistoria | None':
        return self._vistoria_final

    @vistoria_final.setter
    def vistoria_final(self, value: 'Vistoria'):
        self._vistoria_final = value

    @property
    def estaAtivo(self) -> bool:
        return self._estaAtivo

    @estaAtivo.setter
    def estaAtivo(self, value: bool):
        self._estaAtivo = value
