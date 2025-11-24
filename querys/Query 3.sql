-- ============================================================
-- Extras para Controle de Acesso (MariaDB)
-- Inclui: lookup enums, triggers automáticas, procedures,
-- views para dashboard, audit logs, inserts iniciais, roles.
-- Rode este script dentro do DB controle_acesso (USE controle_acesso;)
-- ============================================================

USE controle_acesso;

-- =========================
-- 1) TABELAS DE LOOKUP (ENUMS padronizados)
-- =========================
CREATE TABLE IF NOT EXISTS lk_tipo_empresa (
  tipo VARCHAR(50) PRIMARY KEY
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS lk_tipo_usuario (
  tipo VARCHAR(50) PRIMARY KEY
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS lk_perfil_acesso (
  perfil VARCHAR(50) PRIMARY KEY
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS lk_tipo_acesso (
  tipo VARCHAR(50) PRIMARY KEY
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS lk_tipo_servico (
  tipo VARCHAR(50) PRIMARY KEY
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Popula valores padrão (se quiser editar, remova os inserts duplicados)
INSERT IGNORE INTO lk_tipo_empresa (tipo) VALUES
  ('transportadora'),('visitada'),('prestadora'),('interna');

INSERT IGNORE INTO lk_tipo_usuario (tipo) VALUES
  ('funcionario'),('terceiro'),('visitante'),('admin'),('seguranca'),('operador');

INSERT IGNORE INTO lk_perfil_acesso (perfil) VALUES
  ('admin'),('seguranca'),('operador'),('consulta');

INSERT IGNORE INTO lk_tipo_acesso (tipo) VALUES
  ('pedestre'),('visitante');

INSERT IGNORE INTO lk_tipo_servico (tipo) VALUES
  ('interno'),('visitante'),('entrega'),('coleta'),('manutencao');

-- =========================
-- 2) TABELA DE AUDITORIA (auditoria de inserts/updates/deletes)
-- =========================
CREATE TABLE IF NOT EXISTS audit_logs (
  id_audit BIGINT AUTO_INCREMENT PRIMARY KEY,
  tabela VARCHAR(100) NOT NULL,
  operacao ENUM('INSERT','UPDATE','DELETE') NOT NULL,
  registro_id VARCHAR(100),
  dados_antigos JSON NULL,
  dados_novos JSON NULL,
  usuario_executou VARCHAR(100) DEFAULT NULL,
  data_execucao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Função utilitária para converter OLD/NEW em JSON não disponível em MariaDB clássico,
-- então os triggers irão construir JSON com CONCAT (simples). Ajuste conforme necessidade.

-- =========================
-- 3) TRIGGERS DE AUDITORIA (exemplo para usuarios, veiculos, acessos_pessoais, acessos_veiculares)
-- =========================
DELIMITER $$

-- Usuarios
CREATE TRIGGER trg_audit_usuarios_insert
AFTER INSERT ON usuarios
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs(tabela, operacao, registro_id, dados_novos, usuario_executou)
    VALUES('usuarios','INSERT',NEW.id_usuario, CONCAT('{\"nome\":\"',NEW.nome,'\",\"documento\":\"',NEW.documento,'\"}'),NULL);
END$$

CREATE TRIGGER trg_audit_usuarios_update
AFTER UPDATE ON usuarios
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs(tabela, operacao, registro_id, dados_antigos, dados_novos, usuario_executou)
    VALUES('usuarios','UPDATE',OLD.id_usuario,
      CONCAT('{\"nome\":\"',OLD.nome,'\",\"documento\":\"',OLD.documento,'\"}'),
      CONCAT('{\"nome\":\"',NEW.nome,'\",\"documento\":\"',NEW.documento,'\"}'),
      NULL);
END$$

CREATE TRIGGER trg_audit_usuarios_delete
AFTER DELETE ON usuarios
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs(tabela, operacao, registro_id, dados_antigos, usuario_executou)
    VALUES('usuarios','DELETE',OLD.id_usuario, CONCAT('{\"nome\":\"',OLD.nome,'\",\"documento\":\"',OLD.documento,'\"}'),NULL);
END$$

-- Veiculos
CREATE TRIGGER trg_audit_veiculos_insert
AFTER INSERT ON veiculos
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs(tabela, operacao, registro_id, dados_novos)
    VALUES('veiculos','INSERT',NEW.id_veiculo, CONCAT('{\"placa\":\"',NEW.placa,'\",\"ano\":\"',NEW.ano,'\"}'));
END$$

CREATE TRIGGER trg_audit_veiculos_update
AFTER UPDATE ON veiculos
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs(tabela, operacao, registro_id, dados_antigos, dados_novos)
    VALUES('veiculos','UPDATE',OLD.id_veiculo,
      CONCAT('{\"placa\":\"',OLD.placa,'\",\"ano\":\"',OLD.ano,'\"}'),
      CONCAT('{\"placa\":\"',NEW.placa,'\",\"ano\":\"',NEW.ano,'\"}'));
END$$

CREATE TRIGGER trg_audit_veiculos_delete
AFTER DELETE ON veiculos
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs(tabela, operacao, registro_id, dados_antigos)
    VALUES('veiculos','DELETE',OLD.id_veiculo, CONCAT('{\"placa\":\"',OLD.placa,'\",\"ano\":\"',OLD.ano,'\"}'));
END$$

-- Acessos pessoais
CREATE TRIGGER trg_audit_acessos_pessoais_insert
AFTER INSERT ON acessos_pessoais
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs(tabela, operacao, registro_id, dados_novos)
    VALUES('acessos_pessoais','INSERT',NEW.id_acesso_pessoal,
      CONCAT('{\"id_usuario\":',NEW.id_usuario,',\"hora_entrada\":\"',NEW.hora_entrada,'\"}'));
END$$

CREATE TRIGGER trg_audit_acessos_pessoais_update
AFTER UPDATE ON acessos_pessoais
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs(tabela, operacao, registro_id, dados_antigos, dados_novos)
    VALUES('acessos_pessoais','UPDATE',OLD.id_acesso_pessoal,
      CONCAT('{\"hora_entrada\":\"',OLD.hora_entrada,'\",\"hora_saida\":\"',OLD.hora_saida,'\"}'),
      CONCAT('{\"hora_entrada\":\"',NEW.hora_entrada,'\",\"hora_saida\":\"',NEW.hora_saida,'\"}'));
END$$

-- Acessos veiculares
CREATE TRIGGER trg_audit_acessos_veiculares_insert
AFTER INSERT ON acessos_veiculares
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs(tabela, operacao, registro_id, dados_novos)
    VALUES('acessos_veiculares','INSERT',NEW.id_acesso_veiculo,
      CONCAT('{\"id_veiculo\":',NEW.id_veiculo,',\"placa\":\"',NEW.placa,'\",\"hora_entrada\":\"',NEW.hora_entrada,'\"}'));
END$$

CREATE TRIGGER trg_audit_acessos_veiculares_update
AFTER UPDATE ON acessos_veiculares
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs(tabela, operacao, registro_id, dados_antigos, dados_novos)
    VALUES('acessos_veiculares','UPDATE',OLD.id_acesso_veiculo,
      CONCAT('{\"hora_entrada\":\"',OLD.hora_entrada,'\",\"hora_saida\":\"',OLD.hora_saida,'\"}'),
      CONCAT('{\"hora_entrada\":\"',NEW.hora_entrada,'\",\"hora_saida\":\"',NEW.hora_saida,'\"}'));
END$$

DELIMITER ;

-- =========================
-- 4) TRIGGERS AUTOMÁTICOS ÚTEIS
-- - Preencher documento do usuario no acesso pessoal automaticamente
-- - Preencher placa e ano do veículo no acesso veicular automaticamente
-- =========================
DELIMITER $$
CREATE TRIGGER trg_fill_documento_acesso_pessoal
BEFORE INSERT ON acessos_pessoais
FOR EACH ROW
BEGIN
  IF (NEW.documento_usuario IS NULL OR NEW.documento_usuario = '') THEN
    SET NEW.documento_usuario = (SELECT documento FROM usuarios WHERE id_usuario = NEW.id_usuario LIMIT 1);
  END IF;
  -- default hora_entrada se não envio: usa hora atual
  IF (NEW.hora_entrada IS NULL OR NEW.hora_entrada = '') THEN
    SET NEW.hora_entrada = TIME(CURRENT_TIMESTAMP);
  END IF;
END$$

CREATE TRIGGER trg_fill_veiculo_acesso_veicular
BEFORE INSERT ON acessos_veiculares
FOR EACH ROW
BEGIN
  IF (NEW.placa IS NULL OR NEW.placa = '') THEN
    SET NEW.placa = (SELECT placa FROM veiculos WHERE id_veiculo = NEW.id_veiculo LIMIT 1);
  END IF;
  IF (NEW.ano_veiculo IS NULL) THEN
    SET NEW.ano_veiculo = (SELECT ano FROM veiculos WHERE id_veiculo = NEW.id_veiculo LIMIT 1);
  END IF;
  IF (NEW.hora_entrada IS NULL OR NEW.hora_entrada = '') THEN
    SET NEW.hora_entrada = TIME(CURRENT_TIMESTAMP);
  END IF;
END$$
DELIMITER ;

-- =========================
-- 5) STORED PROCEDURES (Registrar entrada/saída)
-- =========================
DELIMITER $$

-- Registrar entrada pedestre/visitante
CREATE PROCEDURE sp_registrar_entrada_pessoal(
  IN p_id_usuario INT,
  IN p_id_empresa_visitada INT,
  IN p_tipo_acesso VARCHAR(50),
  IN p_motivo VARCHAR(255),
  IN p_observacao TEXT
)
BEGIN
  INSERT INTO acessos_pessoais (data_registro, id_usuario, tipo_acesso, id_empresa_visitada, motivo_visita, hora_entrada, observacao)
  VALUES (CURRENT_TIMESTAMP, p_id_usuario, p_tipo_acesso, p_id_empresa_visitada, p_motivo, TIME(CURRENT_TIMESTAMP), p_observacao);
END$$

-- Registrar saída pedestre/visitante (por id_acesso_pessoal)
CREATE PROCEDURE sp_registrar_saida_pessoal(
  IN p_id_acesso INT
)
BEGIN
  UPDATE acessos_pessoais
    SET hora_saida = TIME(CURRENT_TIMESTAMP)
    WHERE id_acesso_pessoal = p_id_acesso AND hora_saida IS NULL;
END$$

-- Registrar entrada veicular
CREATE PROCEDURE sp_registrar_entrada_veiculo(
  IN p_id_veiculo INT,
  IN p_id_responsavel INT,
  IN p_tipo_servico VARCHAR(50),
  IN p_nota_entrada VARCHAR(100),
  IN p_id_transportadora INT,
  IN p_obs TEXT
)
BEGIN
  INSERT INTO acessos_veiculares (data_registro, id_veiculo, placa, id_responsavel, ano_veiculo, hora_entrada, tipo_servico, nota_fiscal_entrada, id_transportadora, observacao)
  VALUES (CURRENT_TIMESTAMP, p_id_veiculo,
    (SELECT placa FROM veiculos WHERE id_veiculo = p_id_veiculo LIMIT 1),
    p_id_responsavel,
    (SELECT ano FROM veiculos WHERE id_veiculo = p_id_veiculo LIMIT 1),
    TIME(CURRENT_TIMESTAMP),
    p_tipo_servico,
    p_nota_entrada,
    p_id_transportadora,
    p_obs);
END$$

-- Registrar saída veicular (por id_acesso_veiculo)
CREATE PROCEDURE sp_registrar_saida_veiculo(
  IN p_id_acesso_veiculo INT,
  IN p_nota_saida VARCHAR(100)
)
BEGIN
  UPDATE acessos_veiculares
    SET hora_saida = TIME(CURRENT_TIMESTAMP),
        nota_fiscal_saida = COALESCE(p_nota_saida, nota_fiscal_saida)
    WHERE id_acesso_veiculo = p_id_acesso_veiculo AND hora_saida IS NULL;
END$$

DELIMITER ;

-- =========================
-- 6) VIEWS PARA DASHBOARD / RELATÓRIO
-- =========================
-- Acessos ativos (sem hora_saida)
CREATE OR REPLACE VIEW vw_acessos_ativos AS
SELECT 'pessoal' AS tipo, ap.id_acesso_pessoal AS id_acesso, ap.data_registro, ap.id_usuario AS id_entidade,
       u.nome AS nome_entidade, ap.tipo_acesso AS sub_tipo, ap.hora_entrada, ap.hora_saida, e.nome_empresa AS empresa_visitada, ap.observacao
FROM acessos_pessoais ap
LEFT JOIN usuarios u ON u.id_usuario = ap.id_usuario
LEFT JOIN empresas e ON e.id_empresa = ap.id_empresa_visitada
WHERE ap.hora_saida IS NULL
UNION ALL
SELECT 'veicular' AS tipo, av.id_acesso_veiculo AS id_acesso, av.data_registro, av.id_veiculo AS id_entidade,
       v.placa AS nome_entidade, av.tipo_servico AS sub_tipo, av.hora_entrada, av.hora_saida, ep.nome_empresa AS empresa_visitada, av.observacao
FROM acessos_veiculares av
LEFT JOIN veiculos v ON v.id_veiculo = av.id_veiculo
LEFT JOIN empresas ep ON ep.id_empresa = av.id_transportadora
WHERE av.hora_saida IS NULL;

-- Últimas 24h (todos)
CREATE OR REPLACE VIEW vw_acessos_ultimas_24h AS
SELECT 'pessoal' AS tipo, ap.id_acesso_pessoal AS id_acesso, ap.data_registro, u.nome, ap.hora_entrada, ap.hora_saida, ap.motivo_visita
FROM acessos_pessoais ap
LEFT JOIN usuarios u ON u.id_usuario = ap.id_usuario
WHERE ap.data_registro >= (NOW() - INTERVAL 24 HOUR)
UNION ALL
SELECT 'veicular' AS tipo, av.id_acesso_veiculo AS id_acesso, av.data_registro, v.placa, av.hora_entrada, av.hora_saida, av.tipo_servico
FROM acessos_veiculares av
LEFT JOIN veiculos v ON v.id_veiculo = av.id_veiculo
WHERE av.data_registro >= (NOW() - INTERVAL 24 HOUR);

-- Resumo por empresa (total acessos hoje)
CREATE OR REPLACE VIEW vw_resumo_por_empresa AS
SELECT ep.id_empresa, ep.nome_empresa,
  (SELECT COUNT(*) FROM acessos_pessoais ap WHERE ap.id_empresa_visitada = ep.id_empresa AND DATE(ap.data_registro)=CURRENT_DATE) AS acessos_pessoais_hoje,
  (SELECT COUNT(*) FROM acessos_veiculares av WHERE av.id_transportadora = ep.id_empresa AND DATE(av.data_registro)=CURRENT_DATE) AS acessos_veiculos_hoje
FROM empresas ep;

-- =========================
-- 7) INSERTS INICIAIS (admin, empresa padrão, transportadora, veículo)
-- =========================
-- Empresa padrão (visitada)
INSERT IGNORE INTO empresas (nome_empresa, cnpj, tipo_empresa, responsavel, contato)
  VALUES ('Empresa Padrão SA','00.000.000/0000-00','visitada','Responsável Padrão','(11) 0000-0000');

-- Transportadora exemplo
INSERT IGNORE INTO empresas (nome_empresa, cnpj, tipo_empresa, responsavel, contato)
  VALUES ('Transportadora Exemplo LTDA','11.111.111/1111-11','transportadora','Chefe Logística','(11) 1111-1111');

-- Usuário admin (senha_hash deve ser gerada por seu método, aqui um placeholder)
INSERT IGNORE INTO usuarios (nome, documento, tipo_usuario, login, senha_hash, perfil_acesso, empresa_origem, contato)
  VALUES ('Admin Sistema','00000000000','admin','admin',SHA2('senhaAdmin@123',256),'admin', NULL, '(11) 99999-9999');

-- Usuário responsável por veículo
INSERT IGNORE INTO usuarios (nome, documento, tipo_usuario, login, perfil_acesso, empresa_origem)
  VALUES ('Motorista Exemplo','22222222222','terceiro','motorista_ex','consulta', (SELECT id_empresa FROM empresas WHERE nome_empresa='Transportadora Exemplo LTDA' LIMIT 1));

-- Veículo exemplo
INSERT IGNORE INTO veiculos (placa, modelo, ano, id_responsavel)
  VALUES ('ABC1D23','Caminhão T','2018', (SELECT id_usuario FROM usuarios WHERE nome='Motorista Exemplo' LIMIT 1));

-- =========================
-- 8) POLÍTICAS DE SEGURANÇA SQL (exemplo de roles/grants) -- ajuste conforme seu ambiente
-- =========================
-- OBS: criação de users/roles pode requerer permissões de root no servidor.
-- Exemplos comentados (descomente e ajuste nomes/hosts conforme necessário).
/*
CREATE USER 'app_reader'@'%' IDENTIFIED BY 'troque_senha_reader';
CREATE USER 'app_writer'@'%' IDENTIFIED BY 'troque_senha_writer';

GRANT SELECT ON controle_acesso.* TO 'app_reader'@'%';
GRANT SELECT, INSERT, UPDATE ON controle_acesso.acessos_pessoais TO 'app_writer'@'%';
GRANT SELECT, INSERT, UPDATE ON controle_acesso.acessos_veiculares TO 'app_writer'@'%';
-- Crie roles no nível do servidor se MariaDB suportar e associe usuários.
FLUSH PRIVILEGES;
*/

-- =========================
-- 9) INDICES RECOMENDADOS (caso não existam)
-- =========================
CREATE INDEX IF NOT EXISTS idx_acessos_pessoais_data ON acessos_pessoais (data_registro);
CREATE INDEX IF NOT EXISTS idx_acessos_veiculares_data ON acessos_veiculares (data_registro);

-- =========================
-- 10) SUGESTÕES OPERACIONAIS
-- - Faça backup antes de rodar em produção.
-- - A senha do admin inserida é um placeholder: substitua por hash seguro e use MFA.
-- - Considere transformar campos sensíveis (documento) com criptografia a nível de aplicação.
-- - Para alto volume, armazene audit_logs em tabela particionada por data.
-- - Se preferir, convertemos triggers de audit para usar filas (rabbit/kafka) para processamento assíncrono.
-- =========================

-- ============================================================
-- FIM DO SCRIPT
-- ============================================================
