# Funcionalidades - Página de Acesso Pessoal

## Campos Implementados

### 1. **Pesquisar Usuário** (id_usuario)
- Campo de busca com autocompletar
- Busca por:
  - Nome completo
  - Documento (CPF/CNPJ)
  - Login do usuário
- Lista filtrada em dropdown
- Seleção automática do ID do usuário
- Botão para limpar seleção

### 2. **Documento do Usuário** (documento_usuario)
- Campo de apenas leitura
- Preenchido automaticamente quando usuário é selecionado
- Traz o documento do usuário selecionado

### 3. **Tipo de Acesso** (id_tipo_acesso)
- Dropdown com tipos de serviço da tabela `lu_tipos_servico`
- Campos obrigatórios:
  - Visita
  - Manutenção
  - Entrega
  - (outros conforme cadastrado)

### 4. **Pesquisar Empresa Visitada** (id_empresa_visitada)
- Campo de busca com autocompletar (opcional)
- Busca por nome da empresa
- Lista filtrada em dropdown
- Seleção automática do ID da empresa
- Botão para limpar seleção
- Campo pode ser deixado em branco

### 5. **Motivo da Visita** (motivo_visita)
- Campo de texto livre
- Exemplo: "Apresentação comercial", "Reunião", etc
- Opcional

### 6. **Observação** (observacao)
- Campo de texto multilinha
- Informações adicionais sobre o acesso
- Opcional

### 7. **Data/Hora** (hora_entrada)
- Preenchida automaticamente com CURRENT_TIMESTAMP
- Campo oculto no formulário (backend trata)

## Botões de Ação

### Registrar Acesso
- Desabilitado até que um usuário seja selecionado
- Registra o acesso pessoal no sistema

### Cadastrar Novo Usuário
- Botão secundário (laranja)
- Redireciona para página de "Gestão de Usuários"
- Permite cadastrar novo usuário se não existir
- Após cadastro, usuário volta para formulário de acesso pessoal

## Validações

✓ Usuário é obrigatório
✓ Tipo de acesso é obrigatório
✓ Empresa visitada é opcional
✓ Motivo da visita é opcional
✓ Observação é opcional
✓ Data/hora automática no servidor

## Fluxo de Uso

1. Usuário acessa página de "Acessos Pessoais"
2. Digite o nome, documento ou login do usuário na busca
3. Selecione o usuário na lista dropdown
4. Documento é preenchido automaticamente
5. Escolha o tipo de acesso
6. (Opcional) Pesquise e selecione empresa visitada
7. (Opcional) Preencha motivo da visita e observação
8. Clique em "Registrar Acesso"
9. Se usuário não existir, clique em "Cadastrar Novo Usuário" para ir à página de gestão

## Melhorias de UX

- Busca em tempo real com filtros
- Dropdown com seleção visual
- Campos disabled quando não aplicável
- Mensagens claras de validação
- Cores visuais para indicar seleção
- Opção de limpar seleção
- Redirecionamento para cadastro de novos usuários
- Feedback ao usuário após registro bem-sucedido

## Backend - Campos Esperados

```json
{
  "id_usuario": 1,
  "documento_usuario": "12345678900",
  "id_tipo_acesso": 1,
  "id_empresa_visitada": null,
  "motivo_visita": "Reunião",
  "observacao": "Visitou a filial de São Paulo"
}
```

Nota: `data_registro` e `hora_entrada` são preenchidas automaticamente no servidor com CURRENT_TIMESTAMP.
