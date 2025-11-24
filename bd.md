📘 Documentação Revisada – Banco de Dados do App de Controle de Acesso
🔹 1. Tabela: usuarios

Armazena todas as pessoas cadastradas no sistema (funcionários, terceiros, visitantes e também usuários do app).

Campos:

id_usuario (PK)

nome – Nome completo

documento – CPF/RG

tipo_usuario – funcionário | terceiro | visitante | administrador | segurança | operador

login – Usuário do app

senha_hash – Senha criptografada

perfil_acesso – nível de permissão no app

empresa_origem (FK → empresas.id_empresa) – opcional (para terceiros e visitantes)

contato – Telefone/E-mail

data_cadastro – Data e hora do registro

Obs: visitants agora são apenas um tipo dentro dessa tabela.

🔹 2. Tabela: veiculos

Registro dos veículos vinculados a usuários.

Campos:

id_veiculo (PK)

placa – única

modelo

ano

id_responsavel (FK → usuarios.id_usuario)

data_cadastro

🔹 3. Tabela: empresas

Empresas envolvidas no fluxo de acesso.

Campos:

id_empresa (PK)

nome_empresa

cnpj

tipo_empresa – transportadora | empresa visitada | prestadora | interna

responsavel – opcional

contato – opcional

data_cadastro

🔹 4. Tabela: acessos_pessoais

Registro de entrada/saída de pessoas a pé, sem veículo.

Campos:

id_acesso_pessoal (PK)

data_registro – Data/hora completa padrão brasileiro

id_usuario (FK → usuarios.id_usuario)

documento_usuario – preenchido via FK

tipo_acesso – pedestre | visitante

id_empresa_visitada (FK → empresas.id_empresa)

motivo_visita

hora_entrada

hora_saida (nulo se não saiu ainda)

observacao

🔹 5. Tabela: acessos_veiculares

Registro de veículos entrando e saindo da empresa.

Campos:

id_acesso_veiculo (PK)

data_registro – Data/hora completa

id_veiculo (FK → veiculos.id_veiculo)

placa – puxado automaticamente

id_responsavel (FK → usuarios.id_usuario) – motorista/vinculado

ano_veiculo – do cadastro

hora_entrada

hora_saida

tipo_servico – interno | visitante | entrega | coleta | manutenção

nota_fiscal_entrada – opcional

nota_fiscal_saida – opcional

id_transportadora (FK → empresas.id_empresa)

observacao

🔹 6. Mapeamento das FKs
Tabela	Campo FK	Referência
usuarios	empresa_origem	empresas.id_empresa
veiculos	id_responsavel	usuarios.id_usuario
acessos_pessoais	id_usuario	usuarios.id_usuario
acessos_pessoais	id_empresa_visitada	empresas.id_empresa
acessos_veiculares	id_veiculo	veiculos.id_veiculo
acessos_veiculares	id_responsavel	usuarios.id_usuario
acessos_veiculares	id_transportadora	empresas.id_empresa
🔹 7. Regras Gerais

Data e hora sempre no formato: DD/MM/YYYY HH:MM:SS.

Usuários do app ficam na mesma tabela de pessoas, diferenciados por perfil_acesso.

Placa, documento e nome sempre vêm das tabelas relacionadas, nunca digitados manualmente.

Notas fiscais são opcionais.

Serviços e motivos devem ser padrões pré-definidos para evitar divergência.

Observação é campo livre.