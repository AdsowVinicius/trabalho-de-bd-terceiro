USE controle_acesso;

-- ==vw_acessos_pessoais_detalhado==========================================================
-- VIEW 1: Acessos pessoais detalhados
-- ============================================================

CREATE OR REPLACE VIEW vw_acessos_pessoais_detalhado AS
SELECT 
    ap.id_acesso_pessoal,
    ap.data_registro,
    u.nome AS usuario_nome,
    u.documento AS usuario_documento,
    ap.tipo_acesso,
    e.nome_empresa AS empresa_visitada,
    ap.motivo_visita,
    ap.hora_entrada,
    ap.hora_saida,
    ap.observacao
FROM acessos_pessoais ap
LEFT JOIN usuarios u ON ap.id_usuario = u.id_usuario
LEFT JOIN empresas e ON ap.id_empresa_visitada = e.id_empresa;


-- ============================================================
-- VIEW 2: Acessos veiculares detalhados
-- ============================================================

CREATE OR REPLACE VIEW vw_acessos_veiculares_detalhado AS
SELECT 
    av.id_acesso_veiculo,
    av.data_registro,
    v.placa,
    v.modelo,
    v.ano AS ano_veiculo_cadastro,
    u.nome AS responsavel_nome,
    av.hora_entrada,
    av.hora_saida,
    av.tipo_servico,
    av.nota_fiscal_entrada,
    av.nota_fiscal_saida,
    e.nome_empresa AS transportadora,
    av.observacao
FROM acessos_veiculares av
LEFT JOIN veiculos v ON av.id_veiculo = v.id_veiculo
LEFT JOIN usuarios u ON av.id_responsavel = u.id_usuario
LEFT JOIN empresas e ON av.id_transportadora = e.id_empresa;


-- ============================================================
-- VIEW 3: Usuários com empresa de origem
-- ============================================================

CREATE OR REPLACE VIEW vw_usuarios_com_empresa AS
SELECT
    u.id_usuario,
    u.nome,
    u.documento,
    u.tipo_usuario,
    u.login,
    u.perfil_acesso,
    e.nome_empresa AS empresa_origem,
    u.contato,
    u.data_cadastro
FROM usuarios u
LEFT JOIN empresas e ON u.empresa_origem = e.id_empresa;


-- ============================================================
-- VIEW 4: Veículos com responsável
-- ============================================================

CREATE OR REPLACE VIEW vw_veiculos_com_responsavel AS
SELECT 
    v.id_veiculo,
    v.placa,
    v.modelo,
    v.ano,
    u.nome AS responsavel,
    u.documento,
    v.data_cadastro
FROM veiculos v
LEFT JOIN usuarios u ON v.id_responsavel = u.id_usuario;


-- ============================================================
-- VIEW 5: Relatório geral (acessos pessoais + veiculares)
-- ============================================================

CREATE OR REPLACE VIEW vw_relatorio_geral AS
SELECT
    'PESSOAL' AS tipo,
    ap.id_acesso_pessoal AS id,
    ap.data_registro,
    u.nome AS nome,
    u.documento AS identificacao,
    NULL AS placa,
    ap.hora_entrada,
    ap.hora_saida,
    ap.motivo_visita AS motivo,
    e.nome_empresa AS empresa,
    ap.observacao
FROM acessos_pessoais ap
LEFT JOIN usuarios u ON ap.id_usuario = u.id_usuario
LEFT JOIN empresas e ON ap.id_empresa_visitada = e.id_empresa

UNION ALL

SELECT
    'VEICULO' AS tipo,
    av.id_acesso_veiculo AS id,
    av.data_registro,
    u.nome AS nome_responsavel,
    u.documento AS ident_responsavel,
    v.placa,
    av.hora_entrada,
    av.hora_saida,
    av.tipo_servico AS motivo,
    e.nome_empresa AS transportadora,
    av.observacao
FROM acessos_veiculares av
LEFT JOIN veiculos v ON av.id_veiculo = v.id_veiculo
LEFT JOIN usuarios u ON av.id_responsavel = u.id_usuario
LEFT JOIN empresas e ON av.id_transportadora = e.id_empresa;


-- ============================================================
-- VIEW 6: Visitas ativas (pedestres que ainda não saíram)
-- ============================================================

CREATE OR REPLACE VIEW vw_visitas_ativas AS
SELECT
    ap.id_acesso_pessoal,
    ap.data_registro,
    u.nome AS visitante,
    ap.hora_entrada,
    ap.hora_saida,
    e.nome_empresa AS empresa_visitada
FROM acessos_pessoais ap
LEFT JOIN usuarios u ON ap.id_usuario = u.id_usuario
LEFT JOIN empresas e ON ap.id_empresa_visitada = e.id_empresa
WHERE ap.hora_saida IS NULL;


-- ============================================================
-- VIEW 7: Veículos no pátio (sem saída registrada)
-- ============================================================

CREATE OR REPLACE VIEW vw_veiculos_no_patio AS
SELECT
    av.id_acesso_veiculo,
    av.data_registro,
    v.placa,
    u.nome AS responsavel,
    av.hora_entrada,
    av.hora_saida,
    e.nome_empresa AS transportadora
FROM acessos_veiculares av
LEFT JOIN veiculos v ON av.id_veiculo = v.id_veiculo
LEFT JOIN usuarios u ON av.id_responsavel = u.id_usuario
LEFT JOIN empresas e ON av.id_transportadora = e.id_empresa
WHERE av.hora_saida IS NULL;
