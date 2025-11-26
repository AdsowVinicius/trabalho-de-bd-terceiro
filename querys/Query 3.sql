-- Query-3.sql
USE controle_acesso;
DELIMITER $$

-- TRIGGER: preencher documento_usuario em acessos_pessoais quando inserir
CREATE TRIGGER trg_ap_before_insert
BEFORE INSERT ON acessos_pessoais
FOR EACH ROW
BEGIN
  IF NEW.documento_usuario IS NULL OR NEW.documento_usuario = '' THEN
    SELECT documento INTO @doc FROM usuarios WHERE id_usuario = NEW.id_usuario LIMIT 1;
    SET NEW.documento_usuario = IFNULL(@doc, NEW.documento_usuario);
  END IF;
END$$

-- TRIGGER: preencher placa em acessos_veiculares ao inserir (buscar da tabela veiculos)
CREATE TRIGGER trg_av_before_insert
BEFORE INSERT ON acessos_veiculares
FOR EACH ROW
BEGIN
  IF (NEW.placa IS NULL OR NEW.placa = '') AND NEW.id_veiculo IS NOT NULL THEN
    SELECT placa INTO @pl FROM veiculos WHERE id_veiculo = NEW.id_veiculo LIMIT 1;
    SET NEW.placa = IFNULL(@pl, NEW.placa);
  END IF;
END$$

-- TRIGGERS DE AUDIT para INSERT/UPDATE/DELETE (exemplo genérico usando JSON)
-- helper para INSERT
CREATE TRIGGER trg_audit_insert AFTER INSERT ON usuarios
FOR EACH ROW
BEGIN
  INSERT INTO audit_log (tabela, operacao, id_registro, dados_depois, usuario_responsavel)
    VALUES ('usuarios','INSERT', NEW.id_usuario, JSON_OBJECT('nome',NEW.nome,'documento',NEW.documento), USER());
END$$

CREATE TRIGGER trg_audit_update AFTER UPDATE ON usuarios
FOR EACH ROW
BEGIN
  INSERT INTO audit_log (tabela, operacao, id_registro, dados_antes, dados_depois, usuario_responsavel)
    VALUES ('usuarios','UPDATE', NEW.id_usuario, JSON_OBJECT('nome',OLD.nome,'documento',OLD.documento), JSON_OBJECT('nome',NEW.nome,'documento',NEW.documento), USER());
END$$

CREATE TRIGGER trg_audit_delete AFTER DELETE ON usuarios
FOR EACH ROW
BEGIN
  INSERT INTO audit_log (tabela, operacao, id_registro, dados_antes, usuario_responsavel)
    VALUES ('usuarios','DELETE', OLD.id_usuario, JSON_OBJECT('nome',OLD.nome,'documento',OLD.documento), USER());
END$$

-- Stored Procedure: registrar entrada de visitante (pessoal)
CREATE PROCEDURE sp_registrar_entrada_pessoal(
  p_id_usuario INT,
  p_id_empresa_visitada INT,
  p_motivo VARCHAR(255),
  p_observacao TEXT
)
BEGIN
  INSERT INTO acessos_pessoais (id_usuario, id_empresa_visitada, motivo_visita, hora_entrada, observacao)
  VALUES (p_id_usuario, p_id_empresa_visitada, p_motivo, NOW(), p_observacao);
END$$

-- Stored Procedure: registrar saida de visitante (pessoal) — atualiza hora_saida
CREATE PROCEDURE sp_registrar_saida_pessoal(
  p_id_acesso_pessoal INT
)
BEGIN
  UPDATE acessos_pessoais
    SET hora_saida = NOW()
    WHERE id_acesso_pessoal = p_id_acesso_pessoal;
END$$

-- Stored Procedure: registrar entrada veicular
CREATE PROCEDURE sp_registrar_entrada_veicular(
  p_id_veiculo INT,
  p_id_responsavel INT,
  p_id_tipo_servico INT,
  p_nota_fiscal_entrada VARCHAR(80),
  p_id_transportadora INT,
  p_observacao TEXT
)
BEGIN
  INSERT INTO acessos_veiculares (id_veiculo, id_responsavel, id_tipo_servico, nota_fiscal_entrada, id_transportadora, hora_entrada, observacao)
  VALUES (p_id_veiculo, p_id_responsavel, p_id_tipo_servico, p_nota_fiscal_entrada, p_id_transportadora, NOW(), p_observacao);
END$$

-- Stored Procedure: registrar saida veicular
CREATE PROCEDURE sp_registrar_saida_veicular(
  p_id_acesso_veiculo INT,
  p_nota_fiscal_saida VARCHAR(80)
)
BEGIN
  UPDATE acessos_veiculares
    SET hora_saida = NOW(), nota_fiscal_saida = p_nota_fiscal_saida
    WHERE id_acesso_veiculo = p_id_acesso_veiculo;
END$$

DELIMITER ;

-- SUGESTÃO DE USUÁRIO DB (aplicação) com privilégios restritos
-- Substitua 'senha_segura' antes de usar em produção
CREATE USER IF NOT EXISTS 'app_acesso'@'localhost' IDENTIFIED BY 'senha_segura';
GRANT SELECT, INSERT, UPDATE ON controle_acesso.* TO 'app_acesso'@'localhost';
FLUSH PRIVILEGES;
