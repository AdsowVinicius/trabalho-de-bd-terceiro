# Validações e Padronizações Implementadas

## Users.jsx - Gestão de Usuários

### Nome
- ✅ Obrigatório
- ✅ Mínimo 3 caracteres
- ✅ Máximo 120 caracteres
- ✅ Trim (remove espaços)

### Documento
- ✅ Obrigatório
- ✅ Remove caracteres não numéricos
- ✅ Mínimo 8 dígitos
- ✅ Trim

### Login (apenas usuários internos)
- ✅ Obrigatório para admin, segurança, operador
- ✅ Mínimo 4 caracteres
- ✅ Apenas letras, números, ponto, hífen, underscore
- ✅ Convertido para minúsculas
- ✅ Trim

### Senha (apenas usuários internos)
- ✅ Obrigatória na criação
- ✅ Opcional na edição
- ✅ Mínimo 6 caracteres
- ✅ Trim

### Perfil de Acesso
- ✅ Obrigatório para usuários internos

### Contato
- ✅ Opcional
- ✅ Trim
- ✅ Enviado como null se vazio

---

## Empresas.jsx - Gestão de Empresas

### Nome da Empresa
- ✅ Obrigatório
- ✅ Mínimo 3 caracteres
- ✅ Máximo 120 caracteres
- ✅ Trim

### CNPJ
- ✅ Obrigatório
- ✅ Remove caracteres não numéricos
- ✅ Exatamente 14 dígitos
- ✅ Trim

### Tipo de Empresa
- ✅ Obrigatório

### Responsável
- ✅ Opcional
- ✅ Trim
- ✅ Enviado como null se vazio

### Contato
- ✅ Opcional
- ✅ Trim
- ✅ Enviado como null se vazio

---

## Veiculos.jsx - Gestão de Veículos

### Placa
- ✅ Obrigatória
- ✅ Convertida para MAIÚSCULAS
- ✅ Valida formato: ABC1234 ou ABC1D23
- ✅ Trim

### Modelo
- ✅ Opcional
- ✅ Máximo 100 caracteres
- ✅ Trim
- ✅ Enviado como null se vazio

### Ano
- ✅ Obrigatório
- ✅ Valida intervalo: 1980 até (ano atual + 1)
- ✅ Convertido para número inteiro

### Responsável
- ✅ Obrigatório (selecionado via autocomplete)

---

## AcessoPessoal.jsx - Registrar Acesso Pessoal

### Usuário
- ✅ Obrigatório (selecionado via busca)

### Motivo da Visita
- ✅ Opcional
- ✅ Máximo 200 caracteres
- ✅ Trim
- ✅ Enviado como string vazia se não preenchido

### Observação
- ✅ Opcional
- ✅ Máximo 500 caracteres
- ✅ Trim
- ✅ Enviado como string vazia se não preenchido

### Tipo de Acesso
- ✅ Obrigatório (com valor padrão)

### Empresa Visitada
- ✅ Opcional (selecionada via busca)

---

## Padrões de Validação Aplicados

### Gerais
1. **Trim**: Todos os strings têm espaços em branco removidos antes da validação
2. **Null vs Vazio**: Campos opcionais são enviados como `null` se vazios
3. **Tipos Numéricos**: Convertidos para `parseInt` ou removem caracteres não numéricos
4. **Case Sensitivity**: Login → minúsculas, Placa → maiúsculas
5. **Limites de Caracteres**: Definidos para cada campo específico
6. **Formato**: Validação de regex para login, placa e CNPJ

### Fluxo
1. Validar presença obrigatória
2. Validar comprimento mínimo/máximo
3. Validar formato (se aplicável)
4. Padronizar (trim, case, remoção de caracteres especiais)
5. Enviar ao backend com valores normalizados

### Campos Sem Validação (conforme solicitado)
- Campos com validação implícita do HTML (required, maxlength, type)
- Campos que podem ser deixados vazios sem problema

---

**Status**: ✅ Todas as validações e padronizações implementadas
**Data**: 27/11/2025
