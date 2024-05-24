from uuid import UUID
from infrastructure.configs.connection import Connection
from infrastructure.models.solicitacoes import Solicitacoes


class SolicitacoesRepository:
    def get_all(self) -> list[Solicitacoes]:
        with Connection() as connection:
            return connection.session.query(Solicitacoes).all()

    def get_by_id(self, id: UUID) -> Solicitacoes:
        with Connection() as connection:
            return connection.session.query(Solicitacoes)\
                .filter(Solicitacoes.id == id)\
                .first()

    def insert(self, assist) -> Solicitacoes:
        with Connection() as connection:
            connection.session.add(assist)
            return assist

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            connection.session.query(Solicitacoes).filter(Solicitacoes.id == id).delete()


'''SELECT `CONTRATOS`.id AS `CONTRATOS_id`,\
    `CONTRATOS`.data_inicio AS `CONTRATOS_data_inicio`,\
    `CONTRATOS`.data_fim AS `CONTRATOS_data_fim`,\
    `CONTRATOS`.data_cadastro AS `CONTRATOS_data_cadastro`,\
    `CONTRATOS`.locatario_id AS `CONTRATOS_locatario_id`,\
    `CONTRATOS`.imovel_id AS `CONTRATOS_imovel_id`,\
    `CONTRATOS`.funcionario_criador_id AS `CONTRATOS_funcionario_criador_id`,\
    `CONTRATOS`.vistoria_inicial_id AS `CONTRATOS_vistoria_inicial_id`,\
    `CONTRATOS`.vistoria_final_id AS `CONTRATOS_vistoria_final_id`,\
    `SOLICITACOES`.id AS `SOLICITACOES_id`,\
    `SOLICITACOES`.id_contrato AS `SOLICITACOES_id_contrato`,\
    `SOLICITACOES`.titulo AS `SOLICITACOES_titulo`,\
    `SOLICITACOES`.descricao AS `SOLICITACOES_descricao`,\
    `SOLICITACOES`.status AS `SOLICITACOES_status`,\
    `SOLICITACOES`.prioridade AS `SOLICITACOES_prioridade`,\
    `SOLICITACOES`.data_criacao AS `SOLICITACOES_data_criacao`,\
    `OCORRENCIAS`.id AS `OCORRENCIAS_id`,\
    `OCORRENCIAS`.titulo AS `OCORRENCIAS_titulo`,\
    `OCORRENCIAS`.descricao AS `OCORRENCIAS_descricao`,\
    `OCORRENCIAS`.status AS `OCORRENCIAS_status`,\
    `OCORRENCIAS`.prioridade AS `OCORRENCIAS_prioridade`,\
    `OCORRENCIAS`.data_criacao AS `OCORRENCIAS_data_criacao`,\
    `OCORRENCIAS`.id_contrato AS `OCORRENCIAS_id_contrato`,\
    `LOCATARIOS`.id AS `LOCATARIOS_id`,\
    `LOCATARIOS`.nome AS `LOCATARIOS_nome`,\
    `LOCATARIOS`.data_nascimento AS `LOCATARIOS_data_nascimento`,\
    `IMOVEIS`.id AS `IMOVEIS_id`,\
    `IMOVEIS`.codigo AS `IMOVEIS_codigo`,\
    `IMOVEIS`.endereco AS `IMOVEIS_endereco`
FROM `SOLICITACOES` INNER JOIN `CONTRATOS` ON `CONTRATOS`.id = `SOLICITACOES`.id_contrato INNER JOIN `SOLICITACOES` ON `CONTRATOS`.id = `SOLICITACOES`.id_contrato INNER JOIN `OCORRENCIAS` ON `CONTRATOS`.id = `OCORRENCIAS`.id_contrato INNER JOIN `LOCATARIOS` ON `CONTRATOS`.locatario_id = `LOCATARIOS`.id INNER JOIN `IMOVEIS` ON `CONTRATOS`.imovel_id = `IMOVEIS`.id
'''
