-- ============================================================
-- BANCO DE DADOS: Controle de Acesso
-- MariaDB | UTF8MB4 | InnoDB
-- ============================================================

CREATE DATABASE IF NOT EXISTS controle_acesso
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE controle_acesso;

-- ============================================================
-- TABELA: empresas
-- ============================================================

CREATE TABLE empresas (
    id_empresa INT AUTO_INCREMENT PRIMARY KEY,
    nome_empresa VARCHAR(120) NOT NULL,
    cnpj VARCHAR(18),
    tipo_empresa ENUM('transportadora', 'visitada', 'prestadora', 'interna') NOT NULL DEFAULT 'visitada',
    responsavel VARCHAR(100),
    contato VARCHAR(50),
    data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE (cnpj)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABELA: usuarios
-- ============================================================

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    documento VARCHAR(20) NOT NULL,
    tipo_usuario ENUM('funcionario', 'terceiro', 'visitante', 'admin', 'seguranca', 'operador')
        NOT NULL DEFAULT 'visitante',
    login VARCHAR(50),
    senha_hash VARCHAR(255),
    perfil_acesso ENUM('admin', 'seguranca', 'operador', 'consulta') DEFAULT 'consulta',
    empresa_origem INT,
    contato VARCHAR(50),
    data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_usuario_empresa FOREIGN KEY (empresa_origem)
        REFERENCES empresas(id_empresa)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_usuarios_documento ON usuarios(documento);

-- ============================================================
-- TABELA: veiculos
-- ============================================================

CREATE TABLE veiculos (
    id_veiculo INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(8) NOT NULL UNIQUE,
    modelo VARCHAR(50),
    ano YEAR,
    id_responsavel INT NOT NULL,
    data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_veiculo_responsavel FOREIGN KEY (id_responsavel)
        REFERENCES usuarios(id_usuario)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABELA: acessos_pessoais
-- ============================================================

CREATE TABLE acessos_pessoais (
    id_acesso_pessoal INT AUTO_INCREMENT PRIMARY KEY,
    data_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_usuario INT NOT NULL,
    documento_usuario VARCHAR(20),
    tipo_acesso ENUM('pedestre', 'visitante') NOT NULL DEFAULT 'pedestre',
    id_empresa_visitada INT,
    motivo_visita VARCHAR(255),
    hora_entrada TIME NOT NULL,
    hora_saida TIME DEFAULT NULL,
    observacao TEXT,

    CONSTRAINT fk_acesso_pessoal_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
        ON UPDATE CASCADE ON DELETE CASCADE,

    CONSTRAINT fk_acesso_pessoal_empresa FOREIGN KEY (id_empresa_visitada)
        REFERENCES empresas(id_empresa)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_acessos_pessoais_usuario ON acessos_pessoais(id_usuario);

-- ============================================================
-- TABELA: acessos_veiculares
-- ============================================================

CREATE TABLE acessos_veiculares (
    id_acesso_veiculo INT AUTO_INCREMENT PRIMARY KEY,
    data_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_veiculo INT NOT NULL,
    placa VARCHAR(8),
    id_responsavel INT NOT NULL,
    ano_veiculo YEAR,
    hora_entrada TIME NOT NULL,
    hora_saida TIME DEFAULT NULL,
    tipo_servico ENUM('interno', 'visitante', 'entrega', 'coleta', 'manutencao')
        NOT NULL DEFAULT 'visitante',
    nota_fiscal_entrada VARCHAR(50),
    nota_fiscal_saida VARCHAR(50),
    id_transportadora INT,
    observacao TEXT,

    CONSTRAINT fk_acesso_veiculo_veiculo FOREIGN KEY (id_veiculo)
        REFERENCES veiculos(id_veiculo)
        ON UPDATE CASCADE ON DELETE CASCADE,

    CONSTRAINT fk_acesso_veiculo_responsavel FOREIGN KEY (id_responsavel)
        REFERENCES usuarios(id_usuario)
        ON UPDATE CASCADE ON DELETE CASCADE,

    CONSTRAINT fk_acesso_veiculo_transportadora FOREIGN KEY (id_transportadora)
        REFERENCES empresas(id_empresa)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_acessos_veic_placa ON acessos_veiculares(placa);
CREATE INDEX idx_acessos_veic_veiculo ON acessos_veiculares(id_veiculo);
