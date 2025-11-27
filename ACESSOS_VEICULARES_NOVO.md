# 🚗 Acessos Veiculares - Novas Funcionalidades

## Resumo

O formulário de **Acessos Veiculares** foi completamente reformulado com funcionalidades avançadas de busca e autocomplete, permitindo que o usuário registre acessos de veículos com informações completas e auto-preenchimento inteligente.

---

## Campos do Formulário

### 1️⃣ **Pesquisar Veículo** (Obrigatório)
- **Tipo**: Campo de busca com autocomplete + dropdown
- **Busca por**: Placa ou Modelo
- **Retorna**: ID, Placa, Modelo, Ano
- **Auto-preenchimento**: Ao selecionar um veículo:
  - `placa` é preenchido automaticamente
  - `ano` é preenchido automaticamente
  - `modelo` é preenchido automaticamente
- **Botão**: "Limpar Seleção" para desselecionar
- **Validação**: Submit desabilitado se vazio

### 2️⃣ **Responsável / Motorista** (Obrigatório)
- **Tipo**: Campo de busca com autocomplete + dropdown
- **Busca por**: Nome, Documento ou Login
- **Retorna**: ID, Nome, Documento, Login
- **Exibição na Dropdown**: `Nome (Documento) - Login`
- **Botão**: "Limpar Seleção" para desselecionar
- **Validação**: Submit desabilitado se vazio

### 3️⃣ **Tipo de Serviço** (Obrigatório)
- **Tipo**: Select/Dropdown
- **Valores**: Carregados do banco (ex: "Entrega", "Coleta", etc.)
- **Padrão**: Primeiro tipo disponível

### 4️⃣ **Nota Fiscal Entrada** (Opcional)
- **Tipo**: Campo de texto
- **Placeholder**: "Ex: NF-001234"
- **Tamanho máx**: 80 caracteres

### 5️⃣ **Nota Fiscal Saída** (Opcional)
- **Tipo**: Campo de texto
- **Placeholder**: "Ex: NF-001235"
- **Tamanho máx**: 80 caracteres
- **Nota**: Geralmente preenchido ao registrar a saída do veículo

### 6️⃣ **Pesquisar Transportadora** (Opcional)
- **Tipo**: Campo de busca com autocomplete + dropdown
- **Busca por**: Nome da empresa
- **Retorna**: ID, Nome, CNPJ
- **Exibição na Dropdown**: `Nome (CNPJ)`
- **Botão**: "Limpar Seleção" para desselecionar
- **Nota**: Filtro automático para empresas com tipo "transportadora"

### 7️⃣ **Observação** (Opcional)
- **Tipo**: Textarea
- **Linhas**: 4
- **Placeholder**: "Informações adicionais sobre o acesso"
- **Exemplo**: "Carregamento de 50 caixas", "Retorno do cliente", etc.

---

## Botões de Ação

### ✅ Registrar Acesso Veicular
- **Estado**: Desabilitado até selecionar VEÍCULO e RESPONSÁVEL
- **Ação**: Submete o formulário e cria registro no banco
- **Feedback**: 
  - Sucesso: "Acesso veicular registrado com sucesso"
  - Erro: Mostra mensagem de erro do servidor

### 🚗 Cadastrar Novo Veículo
- **Estado**: Sempre ativo (botão laranja)
- **Ação**: Expande modal com instruções
- **Link**: Navega para página de Gestão de Veículos (quando implementada)
- **Nota**: Atualmente vai para `/users` como placeholder

### 👤 Cadastrar Novo Responsável
- **Estado**: Sempre ativo (botão laranja)
- **Ação**: Expande modal com instruções
- **Link**: Navega para página de Gestão de Usuários
- **Nota**: Permite criar novo motorista/condutor

### 🏢 Cadastrar Nova Transportadora
- **Estado**: Sempre ativo (botão laranja)
- **Ação**: Expande modal com instruções
- **Link**: Navega para página de Gestão de Empresas (quando implementada)
- **Nota**: Atualmente vai para `/users` como placeholder

---

## Endpoints da API

### Lookups
```bash
GET /lookups/veiculos
→ [
    {"id": 2, "placa": "ABC-1234", "ano": 2020, "modelo": "Fiat Uno"},
    {"id": 3, "placa": "XYZ-9876", "ano": 2022, "modelo": "Toyota Hilux"}
  ]

GET /lookups/responsaveis
→ [
    {"id": 3, "nome": "João Silva", "documento": "12345678900", "login": "joao_silva"},
    {"id": 4, "nome": "Maria Santos", "documento": "98765432100", "login": "maria_santos"}
  ]

GET /lookups/transportadoras
→ [
    {"id": 1, "nome": "Empresa Exemplo", "cnpj": "00.000.000/0000-00"},
    {"id": 5, "nome": "Logística XYZ", "cnpj": "11.222.333/0000-44"}
  ]
```

### Criação de Registro
```bash
POST /acessos-veiculares/
{
  "id_veiculo": 2,
  "id_responsavel": 3,
  "id_tipo_servico": 1,
  "nota_fiscal_entrada": "NF-123456",
  "nota_fiscal_saida": null,
  "id_transportadora": 1,
  "observacao": "Entrega de mercadorias"
}
→ Status 201 (Created)
→ Retorna registro criado com id_acesso_veicular, timestamps, etc.
```

---

## Fluxo de Uso

1. **Abrir página** `/acessos-veiculares`
2. **Pesquisar Veículo**:
   - Digitar placa (ex: "ABC") ou modelo (ex: "Fiat")
   - Dropdown aparece com matches
   - Clicar para selecionar
   - Campos placa, ano e modelo são auto-preenchidos
3. **Pesquisar Responsável**:
   - Digitar nome, documento ou login
   - Dropdown aparece com matches
   - Clicar para selecionar
4. **Preencher Tipo de Serviço**:
   - Selecionar na dropdown (já tem valor padrão)
5. **Preencher Notas Fiscais** (opcional):
   - NF Entrada: código da nota fiscal de entrada
   - NF Saída: código da nota fiscal de saída (pode deixar vazio se saída ainda não registrada)
6. **Pesquisar Transportadora** (opcional):
   - Digitar nome da empresa
   - Dropdown aparece
   - Clicar para selecionar
7. **Preencher Observação** (opcional):
   - Adicionar informações relevantes
8. **Clicar em Registrar Acesso Veicular**
   - Formulário é validado
   - Registro é criado no banco
   - Confirmação de sucesso
   - Formulário é limpo para novo registro

---

## Tratamento de Erros

### Veículo Não Encontrado
- Clique em **"Cadastrar Novo Veículo"**
- Será direcionado para gerenciamento de veículos
- Crie um novo veículo e retorne ao formulário

### Responsável Não Encontrado
- Clique em **"Cadastrar Novo Responsável"**
- Será direcionado para gerenciamento de usuários
- Crie um novo motorista/condutor e retorne

### Transportadora Não Encontrada
- Clique em **"Cadastrar Nova Transportadora"**
- Será direcionado para gerenciamento de empresas
- Crie uma nova empresa com tipo "Transportadora" e retorne

---

## Melhorias Futuras

- [ ] Página dedicada para gestão de veículos
- [ ] Página dedicada para gestão de empresas (transportadoras)
- [ ] Campos adicionais: peso da carga, dimensões, foto do veículo
- [ ] Validação de placa (formato brasileiro)
- [ ] Histórico de acessos do veículo
- [ ] Relatórios de acessos por transportadora
- [ ] QR code para entrada/saída rápida
- [ ] Integração com GPS para rastreamento

---

## Testes Realizados ✅

- ✅ Login com porteiro_teste
- ✅ Fetch de veículos (/lookups/veiculos)
- ✅ Fetch de responsáveis (/lookups/responsaveis)
- ✅ Fetch de transportadoras (/lookups/transportadoras)
- ✅ POST /acessos-veiculares/ com todos os campos
- ✅ Frontend carrega e renderiza corretamente
- ✅ Autocomplete funciona com filtros
- ✅ Auto-preenchimento de campos
- ✅ Validação de submit (desabilitado quando necessário)

---

## Exemplo Prático

### Cenário: Chegada de um caminhão de entrega

**Passo 1**: Abrir formulário  
**Passo 2**: Pesquisar por placa `ABC-1234` → Seleciona
- Auto-preenchimento: Placa: ABC-1234, Ano: 2020, Modelo: Fiat Uno

**Passo 3**: Pesquisar motorista `João` → Seleciona João Silva (doc: 12345678900)

**Passo 4**: Tipo de Serviço: "Entrega" (já selecionado)

**Passo 5**: NF Entrada: `NF-001234`

**Passo 6**: Pesquisar transportadora `Logística` → Seleciona Logística XYZ

**Passo 7**: Observação: "50 caixas de mercadoria - Entrega para loja Centro"

**Passo 8**: Clicar **Registrar Acesso Veicular**

✅ **Resultado**: Acesso registrado no banco com hora_entrada automática

---

**Status**: ✅ COMPLETO E TESTADO  
**Data**: 27 de Novembro de 2025
