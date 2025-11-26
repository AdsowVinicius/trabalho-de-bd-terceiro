-- ===========================================
-- Query-1.sql — Banco controle_acesso (MariaDB)
-- 100% Funcionando
-- ===========================================

-- Corrige o sql_mode SEM o valor inválido
SET @@session.sql_mode =
'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION';

CREATE DATABASE IF NOT EXISTS controle_acesso
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE controle_acesso;

-- ===========================================
-- LOOKUP TABLES (Enum padronizado)
-- ===========================================

CREATE TABLE lu_tipos_empresa (
  id INT AUTO_INCREMENT PRIMARY KEY,
  chave VARCHAR(50) NOT NULL UNIQUE,
  descricao VARCHAR(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lu_tipos_usuario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  chave VARCHAR(50) NOT NULL UNIQUE,
  descricao VARCHAR(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lu_perfis_acesso (
  id INT AUTO_INCREMENT PRIMARY KEY,
  chave VARCHAR(50) NOT NULL UNIQUE,
  descricao VARCHAR(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lu_tipos_servico (
  id INT AUTO_INCREMENT PRIMARY KEY,
  chave VARCHAR(50) NOT NULL UNIQUE,
  descricao VARCHAR(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ===========================================
-- EMPRESAS
-- ===========================================

CREATE TABLE empresas (
  id_empresa INT AUTO_INCREMENT PRIMARY KEY,
  nome_empresa VARCHAR(120) NOT NULL,
  cnpj VARCHAR(18),
  id_tipo_empresa INT NOT NULL,
  responsavel VARCHAR(100),
  contato VARCHAR(50),
  data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (cnpj),
  CONSTRAINT fk_empresas_tipo FOREIGN KEY (id_tipo_empresa)
      REFERENCES lu_tipos_empresa(id)
      ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ===========================================
-- USUARIOS (App)
-- ===========================================

CREATE TABLE usuarios (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  documento VARCHAR(30) NOT NULL,
  id_tipo_usuario INT NOT NULL,
  login VARCHAR(80) UNIQUE,
  senha_hash VARCHAR(255),
  id_perfil_acesso INT NOT NULL,
  empresa_origem INT,
  contato VARCHAR(60),
  ativo TINYINT(1) NOT NULL DEFAULT 1,
  data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_usuario_tipo FOREIGN KEY (id_tipo_usuario)
      REFERENCES lu_tipos_usuario(id)
      ON UPDATE CASCADE ON DELETE RESTRICT,

  CONSTRAINT fk_usuario_perfil FOREIGN KEY (id_perfil_acesso)
      REFERENCES lu_perfis_acesso(id)
      ON UPDATE CASCADE ON DELETE RESTRICT,

  CONSTRAINT fk_usuario_empresa FOREIGN KEY (empresa_origem)
      REFERENCES empresas(id_empresa)
      ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_usuarios_documento ON usuarios(documento);

-- ===========================================
-- VEÍCULOS
-- ===========================================

CREATE TABLE veiculos (
  id_veiculo INT AUTO_INCREMENT PRIMARY KEY,
  placa VARCHAR(10) NOT NULL UNIQUE,
  modelo VARCHAR(80),
  ano YEAR,
  id_responsavel INT NOT NULL,
  data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_veiculo_responsavel FOREIGN KEY (id_responsavel)
      REFERENCES usuarios(id_usuario)
      ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ===========================================
-- ACESSOS PESSOAIS
-- ===========================================

CREATE TABLE acessos_pessoais (
  id_acesso_pessoal INT AUTO_INCREMENT PRIMARY KEY,
  data_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  id_usuario INT NOT NULL,
  documento_usuario VARCHAR(30),
  id_tipo_acesso INT NOT NULL,
  id_empresa_visitada INT,
  motivo_visita VARCHAR(255),
  hora_entrada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  hora_saida DATETIME,
  observacao TEXT,

  CONSTRAINT fk_acessos_pessoais_usuario FOREIGN KEY (id_usuario)
      REFERENCES usuarios(id_usuario)
      ON UPDATE CASCADE ON DELETE RESTRICT,

  CONSTRAINT fk_acessos_pessoais_empresa FOREIGN KEY (id_empresa_visitada)
      REFERENCES empresas(id_empresa)
      ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_acessos_pessoais_usuario ON acessos_pessoais(id_usuario);

-- ===========================================
-- ACESSOS VEICULARES
-- ===========================================

CREATE TABLE acessos_veiculares (
  id_acesso_veiculo INT AUTO_INCREMENT PRIMARY KEY,
  data_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  id_veiculo INT NOT NULL,
  placa VARCHAR(10),
  id_responsavel INT NOT NULL,
  ano_veiculo YEAR,
  hora_entrada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  hora_saida DATETIME,
  id_tipo_servico INT NOT NULL,
  nota_fiscal_entrada VARCHAR(80),
  nota_fiscal_saida VARCHAR(80),
  id_transportadora INT,
  observacao TEXT,

  CONSTRAINT fk_acesso_veic_veiculo FOREIGN KEY (id_veiculo)
      REFERENCES veiculos(id_veiculo)
      ON UPDATE CASCADE ON DELETE RESTRICT,

  CONSTRAINT fk_acesso_veic_responsavel FOREIGN KEY (id_responsavel)
      REFERENCES usuarios(id_usuario)
      ON UPDATE CASCADE ON DELETE RESTRICT,

  CONSTRAINT fk_acesso_veic_transportadora FOREIGN KEY (id_transportadora)
      REFERENCES empresas(id_empresa)
      ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_acessos_veic_placa ON acessos_veiculares(placa);
CREATE INDEX idx_acessos_veic_veiculo ON acessos_veiculares(id_veiculo);

-- ===========================================
-- AUDITORIA
-- ===========================================

CREATE TABLE audit_log (
  id_log BIGINT AUTO_INCREMENT PRIMARY KEY,
  tabela VARCHAR(100) NOT NULL,
  operacao ENUM('INSERT','UPDATE','DELETE') NOT NULL,
  id_registro VARCHAR(100),
  dados_antes JSON,
  dados_depois JSON,
  usuario_responsavel VARCHAR(120),
  data_operacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ===========================================
-- INSERTS INICIAIS
-- ===========================================

INSERT INTO lu_tipos_empresa (chave,descricao) VALUES
  ('transportadora','Transportadora'),
  ('visitada','Empresa Visitada'),
  ('prestadora','Prestadora de Serviço'),
  ('interna','Interna');

INSERT INTO lu_tipos_usuario (chave,descricao) VALUES
  ('funcionario','Funcionário'),
  ('terceiro','Terceiro'),
  ('visitante','Visitante'),
  ('admin','Administrador'),
  ('seguranca','Segurança'),
  ('operador','Operador');

INSERT INTO lu_perfis_acesso (chave,descricao) VALUES
  ('admin','Administrador'),
  ('seguranca','Segurança'),
  ('operador','Operador'),
  ('consulta','Consulta');

INSERT INTO lu_tipos_servico (chave,descricao) VALUES
  ('interno','Interno'),
  ('visitante','Visitante'),
  ('entrega','Entrega'),
  ('coleta','Coleta'),
  ('manutencao','Manutenção');

-- Empresa padrão (agora usando ID numérico)
INSERT INTO empresas (nome_empresa, cnpj, id_tipo_empresa, responsavel, contato)
VALUES ('Empresa Padrão','00.000.000/0000-00',
        (SELECT id FROM lu_tipos_empresa WHERE chave='visitada'),
        'Administrador','+55 11 0000-0000');

-- Usuário admin
INSERT INTO usuarios (nome, documento, id_tipo_usuario, login, senha_hash,
                      id_perfil_acesso, empresa_origem, contato)
VALUES (
  'Administrador Sistema',
  '00000000000',
  (SELECT id FROM lu_tipos_usuario WHERE chave='admin'),
  'admin',
  '',
  (SELECT id FROM lu_perfis_acesso WHERE chave='admin'),
  1,
  '+55 11 0000-0000'
);
