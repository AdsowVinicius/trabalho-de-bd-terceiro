USE controle_acesso;

------------------------------------------------------------
-- VIEW: acessos pessoais detalhado
------------------------------------------------------------
CREATE OR REPLACE VIEW vw_acessos_pessoais_detalhado AS
SELECT 
    ap.id_acesso_pessoal,
    ap.data_registro,
    u.id_usuario,
    u.nome AS nome_usuario,
    u.documento AS documento_cadastrado,
    ls.chave AS tipo_acesso,
    e.nome_empresa AS empresa_visitada,
    ap.motivo_visita,
    ap.hora_entrada,
    ap.hora_saida,
    ap.observacao
FROM acessos_pessoais ap
JOIN usuarios u 
    ON ap.id_usuario = u.id_usuario
LEFT JOIN empresas e 
    ON ap.id_empresa_visitada = e.id_empresa
LEFT JOIN lu_tipos_servico ls 
    ON ap.id_tipo_acesso = ls.id;   -- <== AQUI ESTAVA O ERRO

------------------------------------------------------------
-- VIEW: acessos veiculares detalhado
------------------------------------------------------------
CREATE OR REPLACE VIEW vw_acessos_veiculares_detalhado AS
SELECT 
    av.id_acesso_veiculo,
    av.data_registro,
    v.id_veiculo,
    v.placa,
    v.modelo,
    v.ano AS ano_cadastrado,
    ur.id_usuario AS id_responsavel,
    ur.nome AS nome_responsavel,
    e.nome_empresa AS transportadora,
    ls.chave AS tipo_servico,
    av.nota_fiscal_entrada,
    av.nota_fiscal_saida,
    av.hora_entrada,
    av.hora_saida,
    av.observacao
FROM acessos_veiculares av
JOIN veiculos v 
    ON av.id_veiculo = v.id_veiculo
JOIN usuarios ur 
    ON av.id_responsavel = ur.id_usuario
LEFT JOIN empresas e 
    ON av.id_transportadora = e.id_empresa
LEFT JOIN lu_tipos_servico ls 
    ON av.id_tipo_servico = ls.id;

------------------------------------------------------------
-- VIEW: visitantes atualmente dentro
------------------------------------------------------------
CREATE OR REPLACE VIEW vw_visitantes_ativos AS
SELECT 
    ap.id_acesso_pessoal,
    u.nome,
    u.documento,
    ap.hora_entrada,
    ap.motivo_visita,
    e.nome_empresa AS empresa_visitada
FROM acessos_pessoais ap
JOIN usuarios u 
    ON ap.id_usuario = u.id_usuario
LEFT JOIN empresas e 
    ON ap.id_empresa_visitada = e.id_empresa
WHERE ap.hora_saida IS NULL;

------------------------------------------------------------
-- VIEW: veiculos atualmente dentro
------------------------------------------------------------
CREATE OR REPLACE VIEW vw_veiculos_ativos AS
SELECT 
    av.id_acesso_veiculo,
    v.placa,
    v.modelo,
    ur.nome AS motorista,
    av.hora_entrada,
    av.id_tipo_servico
FROM acessos_veiculares av
JOIN veiculos v 
    ON av.id_veiculo = v.id_veiculo
JOIN usuarios ur 
    ON av.id_responsavel = ur.id_usuario
WHERE av.hora_saida IS NULL;
