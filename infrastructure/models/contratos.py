from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped
from infrastructure.models import Base
from infrastructure.models.ocorrencias import Ocorrencias
from infrastructure.models.solicitacoes import Solicitacoes
from infrastructure.models.locatarios import Locatarios
from infrastructure.models.imoveis import Imoveis


#Base = declarative_base()

class Contratos(Base):
    __tablename__ = 'CONTRATOS'

    id = Column(String(36), primary_key=True)
    data_inicio = Column(Date, name='data_inicio')
    data_fim = Column(Date, name='data_fim')
    data_cadastro = Column(Date, name='data_cadastro')

    imovel_id = Column(String(36), ForeignKey('IMOVEIS.id'), name='imovel_id')
    imovel = relationship('Imoveis')

    locatario_id = Column(String(36), ForeignKey('LOCATARIOS.id'), name='locatario_id')
    locatario = relationship('Locatarios', back_populates='contratos')

    solicitacoes = relationship('Solicitacoes', cascade='all, delete-orphan')

    ocorrencias = relationship('Ocorrencias', cascade='all, delete-orphan')

    vistoria_inicial_id = Column(String(36), name='vistoria_inicial_id')
    vistoria_final_id = Column(String(36), name='vistoria_final_id')

    '''locatario_id = Column(String(36), ForeignKey('LOCATARIOS.id'), name='locatario_id')
    imovel_id = Column(String(36), ForeignKey('IMOVEIS.id'),name='imovel_id')
    funcionario_criador_id = Column(String(36), ForeignKey('USUARIOS_IDENTITY_INFOS.id'), name='funcionario_criador_id')
    vistoria_inicial_id = Column(String(36), ForeignKey('VISTORIAS.id'), name='vistoria_inicial_id')
    vistoria_final_id = Column(String(36), ForeignKey('VISTORIAS.id'), name='vistoria_final_id')'''

    def __repr__(self):
        return f'''<Contratos(id={self.id},
        data_inicio={self.data_inicio},
        data_fim={self.data_fim},
        data_cadastro={self.data_cadastro},
        vistoria_inicial_id={self.vistoria_inicial_id},
        vistoria_final_id={self.vistoria_final_id},
        imovel_id={self.imovel_id},
        imovel={self.imovel},
        locatario_id={self.locatario_id}
        locatario={self.locatario},
        ocorrencias={self.ocorrencias})>'''
