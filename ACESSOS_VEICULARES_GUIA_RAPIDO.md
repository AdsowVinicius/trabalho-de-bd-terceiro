# 🚀 GUIA RÁPIDO - FORMULÁRIO ACESSOS VEICULARES

## O que foi criado?

Um formulário **completo e inteligente** para registrar acessos de veículos com:
- ✅ Busca automática de veículos
- ✅ Auto-preenchimento de dados do carro
- ✅ Busca de responsáveis (motoristas)
- ✅ Busca de transportadoras
- ✅ 4 botões para cadastrar novos registros
- ✅ Validação inteligente

---

## Como Usar?

### 1. Abrir o Formulário
```
URL: http://localhost:5174/acessos-veiculares
```

### 2. Preencher Veículo (obrigatório)
```
Pesquisar Veiculo: ABC-1234
↓ (dropdown aparece)
ABC-1234 - Fiat Uno (2020)
↓ (click para selecionar)
Resultado: campos preenchidos automaticamente
  Placa: ABC-1234
  Ano: 2020
  Modelo: Fiat Uno
```

### 3. Preencher Responsável (obrigatório)
```
Pesquisar Responsavel: João
↓ (dropdown aparece)
João Silva (12345678900) - joao_silva
↓ (click para selecionar)
Resultado: id_responsavel definido
```

### 4. Preencher Tipo de Serviço (obrigatório)
```
Dropdown já tem valor padrão, ou escolha outro
```

### 5. Preencher Notas Fiscais (opcional)
```
Nota Fiscal Entrada: NF-123456
Nota Fiscal Saida: (deixe vazio se ainda não saiu)
```

### 6. Preencher Transportadora (opcional)
```
Pesquisar Transportadora: Logística
↓ (dropdown aparece)
Logística XYZ (CNPJ...)
↓ (click para selecionar)
```

### 7. Preencher Observação (opcional)
```
Observacao: 50 caixas de mercadoria - Entrega rápida
```

### 8. Registrar
```
Clique em: "Registrar Acesso Veicular"
Resultado: Acesso criado com timestamp automático
```

---

## E se não tiver veículo?

### Clique em: "Cadastrar Novo Veiculo"
- Modal aparece
- Botão leva para gestão de veículos
- Criar novo veiculo lá
- Voltar ao formulário

---

## E se não tiver responsável?

### Clique em: "Cadastrar Novo Responsavel"
- Modal aparece
- Botão leva para gestão de usuários
- Criar novo motorista/condutor lá
- Voltar ao formulário

---

## E se não tiver transportadora?

### Clique em: "Cadastrar Nova Transportadora"
- Modal aparece
- Botão leva para gestão de empresas
- Criar nova transportadora lá
- Voltar ao formulário

---

## Campos Explicados

| Campo | Obrigatório | Busca | Auto-Preenche | Exemplo |
|-------|-------------|-------|---------------|---------|
| Veículo | ✅ | ✅ | placa, ano, modelo | ABC-1234 |
| Placa | Leitura | - | ✅ | ABC-1234 |
| Ano | Leitura | - | ✅ | 2020 |
| Modelo | Leitura | - | ✅ | Fiat Uno |
| Responsável | ✅ | ✅ | - | João Silva |
| Tipo Serviço | ✅ | - | ✅ | Entrega |
| NF Entrada | Não | - | - | NF-001234 |
| NF Saída | Não | - | - | NF-001235 |
| Transportadora | Não | ✅ | - | Logística XYZ |
| Observação | Não | - | - | 50 caixas |

---

## APIs Usadas

```javascript
// Busca veículos
GET /lookups/veiculos
→ [{id, placa, ano, modelo}, ...]

// Busca responsáveis
GET /lookups/responsaveis
→ [{id, nome, documento, login}, ...]

// Busca transportadoras
GET /lookups/transportadoras
→ [{id, nome, cnpj}, ...]

// Registra acesso
POST /acessos-veiculares/
→ 201 (Created)
```

---

## Troubleshooting

### ❌ Dropdown não aparece
→ Certifique que digitou algo no campo
→ Clique no campo para focar

### ❌ Veículo não aparece na busca
→ Use placa ou modelo
→ Ex: "ABC" ou "Fiat"
→ Veículo pode não estar cadastrado

### ❌ Botão de Registrar desabilitado
→ Verifique que VEÍCULO foi selecionado
→ Verifique que RESPONSÁVEL foi selecionado
→ Tipo de Serviço é obrigatório (já tem padrão)

### ❌ Erro ao registrar
→ Veículo ID inválido (já foi deletado?)
→ Responsável ID inválido
→ Tipo de Serviço inválido
→ Veja mensagem de erro para detalhes

---

## Status

✅ **PRONTO PARA USO**

Desenvolvido com:
- FastAPI (Backend)
- React (Frontend)
- MariaDB (Banco de Dados)

Testado e validado ✓

---

**Dúvidas?** Veja `ACESSOS_VEICULARES_NOVO.md` para documentação completa
