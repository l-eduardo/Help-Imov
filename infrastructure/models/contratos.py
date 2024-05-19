from sqlalchemy import Column, Date, ForeignKey, String
from infrastructure.models import Base


#Base = declarative_base()

class Contratos(Base):
    __tablename__ = 'CONTRATOS'

    id = Column(String(36), primary_key=True)
    data_inicio = Column(Date, name='data_inicio')
    data_fim = Column(Date, name='data_fim')
    data_cadastro = Column(Date, name='data_cadastro')
    locatario_id = Column(String(36), name='locatario_id')
    imovel_id = Column(String(36), name='imovel_id')
    funcionario_criador_id = Column(String(36), name='funcionario_criador_id')
    vistoria_inicial_id = Column(String(36), name='vistoria_inicial_id')
    vistoria_final_id = Column(String(36), name='vistoria_final_id')


    '''locatario_id = Column(String(36), ForeignKey('LOCATARIOS.id'), name='locatario_id')
    imovel_id = Column(String(36), ForeignKey('IMOVEIS.id'),name='imovel_id')
    funcionario_criador_id = Column(String(36), ForeignKey('USUARIOS_IDENTITY_INFOS.id'), name='funcionario_criador_id')
    vistoria_inicial_id = Column(String(36), ForeignKey('VISTORIAS.id'), name='vistoria_inicial_id')
    vistoria_final_id = Column(String(36), ForeignKey('VISTORIAS.id'), name='vistoria_final_id')'''
