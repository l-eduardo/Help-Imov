-- Table to store user identity information
CREATE TABLE USUARIOS_IDENTITY_INFOS (
  id varchar(36) PRIMARY KEY,
  email VARCHAR(255),
  senha VARCHAR(255)
);

-- Table for administrators
CREATE TABLE ADMINISTRADORES (
  id varchar(36) PRIMARY KEY,
  nome VARCHAR(255),
  data_nascimento DATE,
  is_root BOOLEAN,
  FOREIGN KEY (id) REFERENCES USUARIOS_IDENTITY_INFOS(id)
);

-- Table for assistants
CREATE TABLE ASSISTENTES (
  id varchar(36) PRIMARY KEY,
  nome VARCHAR(255),
  data_nascimento DATE,
  FOREIGN KEY (id) REFERENCES USUARIOS_IDENTITY_INFOS(id)
);

-- Table for service providers
CREATE TABLE PRESTADORES_SERVICOS (
  id varchar(36) PRIMARY KEY,
  nome VARCHAR(255),
  data_nascimento DATE,
  especialidade VARCHAR(255),
  empresa VARCHAR(255),
  FOREIGN KEY (id) REFERENCES USUARIOS_IDENTITY_INFOS(id)
);

-- Table to link users with occurrences
CREATE TABLE USUARIOS_OCORRENCIAS (
  usuario_id varchar(36) REFERENCES USUARIOS_IDENTITY_INFOS(id),
  ocorrencia_id varchar(36) REFERENCES OCORRENCIAS(id),
  PRIMARY KEY (usuario_id, ocorrencia_id)
);

-- Table for tenants
CREATE TABLE LOCATARIOS (
  id varchar(36) PRIMARY KEY,
  nome VARCHAR(255),
  data_nascimento DATE,
  especialidade VARCHAR(255),
  empresa VARCHAR(255),
  FOREIGN KEY (id) REFERENCES USUARIOS_IDENTITY_INFOS(id)
);

-- Table for properties
CREATE TABLE IMOVEIS (
  id varchar(36) PRIMARY KEY,
  codigo INT,
  endereco VARCHAR(255)
);

-- Table to store images associated with properties
CREATE TABLE IMAGENS (
  id varchar(36) PRIMARY KEY,
  imagem BLOB
);

-- Table for documents
CREATE TABLE DOCUMENTOS (
  id varchar(36) PRIMARY KEY,
  documentos BLOB,
  vistoria_id varchar(36) REFERENCES VISTORIAS(id)
);

-- Table for occurrences
CREATE TABLE OCORRENCIAS (
  id varchar(36) PRIMARY KEY,
  titulo VARCHAR(255),
  descricao VARCHAR(255),
  status VARCHAR(50),
  prioridade VARCHAR(50),
  data_criacao DATE
);

-- Table for requests
CREATE TABLE SOLICITACOES (
  id varchar(36) PRIMARY KEY,
  contrato_id varchar(36) REFERENCES CONTRATOS(id),
  titulo VARCHAR(255),
  descricao VARCHAR(255),
  status VARCHAR(50),
  prioridade VARCHAR(50),
  data_criacao DATE
);

-- Table for contracts
CREATE TABLE CONTRATOS (
  id varchar(36) PRIMARY KEY,
  data_inicio DATE,
  data_fim DATE,
  data_cadastro DATE,
  locatario_id varchar(36) REFERENCES LOCATARIOS(id),
  imovel_id varchar(36) REFERENCES IMOVEIS(id),
  funcionario_criador_id varchar(36) REFERENCES USUARIOS_IDENTITY_INFOS(id),
  vistoria_inicial_id varchar(36) REFERENCES VISTORIAS(id),
  vistoria_final_id varchar(36) REFERENCES VISTORIAS(id)
);

-- Table for property inspections
CREATE TABLE VISTORIAS (
  id varchar(36) PRIMARY KEY,
  contra_vistoria varchar(36) REFERENCES VISTORIAS(id),
  e_contestacao BOOLEAN,
  esta_fechada BOOLEAN,
  imovel_id varchar(36) REFERENCES IMOVEIS(id)
);


SELECT `CONTRATOS`.id AS `CONTRATOS_id`,
    `CONTRATOS`.data_inicio AS `CONTRATOS_data_inicio`,
    `CONTRATOS`.data_fim AS `CONTRATOS_data_fim`,
    `CONTRATOS`.data_cadastro AS `CONTRATOS_data_cadastro`,
    `CONTRATOS`.locatario_id AS `CONTRATOS_locatario_id`,
    `CONTRATOS`.imovel_id AS `CONTRATOS_imovel_id`,
    `CONTRATOS`.funcionario_criador_id AS `CONTRATOS_funcionario_criador_id`,
    `CONTRATOS`.vistoria_inicial_id AS `CONTRATOS_vistoria_inicial_id`,
    `CONTRATOS`.vistoria_final_id AS `CONTRATOS_vistoria_final_id`,
    `SOLICITACOES`.id AS `SOLICITACOES_id`,
    `SOLICITACOES`.id_contrato AS `SOLICITACOES_id_contrato`,
    `SOLICITACOES`.titulo AS `SOLICITACOES_titulo`,
    `SOLICITACOES`.descricao AS `SOLICITACOES_descricao`,
    `SOLICITACOES`.status AS `SOLICITACOES_status`,
    `SOLICITACOES`.prioridade AS `SOLICITACOES_prioridade`,
    `SOLICITACOES`.data_criacao AS `SOLICITACOES_data_criacao`,
    `OCORRENCIAS`.id AS `OCORRENCIAS_id`,
    `OCORRENCIAS`.titulo AS `OCORRENCIAS_titulo`,
    `OCORRENCIAS`.descricao AS `OCORRENCIAS_descricao`,
    `OCORRENCIAS`.status AS `OCORRENCIAS_status`,
    `OCORRENCIAS`.prioridade AS `OCORRENCIAS_prioridade`,
    `OCORRENCIAS`.data_criacao AS `OCORRENCIAS_data_criacao`,
    `OCORRENCIAS`.id_contrato AS `OCORRENCIAS_id_contrato`,
    `LOCATARIOS`.id AS `LOCATARIOS_id`,
    `LOCATARIOS`.nome AS `LOCATARIOS_nome`,
    `LOCATARIOS`.data_nascimento AS `LOCATARIOS_data_nascimento`,
    `IMOVEIS`.id AS `IMOVEIS_id`,
    `IMOVEIS`.codigo AS `IMOVEIS_codigo`,
    `IMOVEIS`.endereco AS `IMOVEIS_endereco`
FROM `SOLICITACOES` INNER JOIN `CONTRATOS` ON `CONTRATOS`.id = `SOLICITACOES`.id_contrato INNER JOIN
`OCORRENCIAS` ON `CONTRATOS`.id = `OCORRENCIAS`.id_contrato INNER JOIN
`LOCATARIOS` ON `CONTRATOS`.locatario_id = `LOCATARIOS`.id INNER JOIN
`IMOVEIS` ON `CONTRATOS`.imovel_id = `IMOVEIS`.id
