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
