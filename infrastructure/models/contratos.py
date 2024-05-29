from sqlalchemy import Column, Date, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, Mapped
from infrastructure.models import Base
from infrastructure.models.vistorias import Vistorias
from infrastructure.models.ocorrencias import Ocorrencias
from infrastructure.models.solicitacoes import Solicitacoes
from infrastructure.models.locatarios import Locatarios
from infrastructure.models.imoveis import Imoveis


class Contratos(Base):
    __tablename__ = 'CONTRATOS'

    id = Column(String(36), primary_key=True)
    data_inicio = Column(Date, name='data_inicio')
    data_fim = Column(Date, name='data_fim')
    data_cadastro = Column(Date, name='data_cadastro')
    esta_ativo = Column(Boolean, name='esta_ativo')

    criador_id = Column(String(36), ForeignKey('USUARIOS_IDENTITY_INFOS.id'), name='criador_id')

    imovel_id = Column(String(36), ForeignKey('IMOVEIS.id'), name='imovel_id')
    imovel = relationship('Imoveis')

    locatario_id = Column(String(36), ForeignKey('LOCATARIOS.id'), name='locatario_id')
    locatario = relationship('Locatarios', back_populates='contratos')

    solicitacoes = relationship('Solicitacoes', cascade='all, delete-orphan')

    ocorrencias = relationship('Ocorrencias', cascade='all, delete-orphan')

    vistoria_inicial_id = Column(String(36), ForeignKey('VISTORIAS.id', ondelete='SET NULL'),
                                 name='vistoria_inicial_id')

    vistoria_inicial = relationship('Vistorias', foreign_keys=[vistoria_inicial_id])

    # erro de não salvar associação de contra_vistoria no banco pode estar aqui
    contra_vistoria_id = Column(String(36), ForeignKey('VISTORIAS.id', ondelete='SET NULL'),
                                             name='contra_vistoria_id')

    contra_vistoria = relationship('Vistorias', foreign_keys=[contra_vistoria_id])
