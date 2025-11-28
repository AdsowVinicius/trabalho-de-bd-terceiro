# 🎨 Guia Visual - Design TERCEIRIZE+

## 🌈 Paleta de Cores em Ação

### Verde Primário (#0B7A47)
```
Uso:
├─ Navegação (background gradient)
├─ Botões primários (submit, novo, criar)
├─ Headers de tabelas
├─ Links ativos
├─ Titles (h1, h2, h3)
└─ Shadows (color accent)
```

### Branco (#FFFFFF)
```
Uso:
├─ Fundo principal de cards
├─ Texto em navegação
├─ Inputs/formulários
├─ Background padrão de modals
└─ Garantia de contraste
```

### Cinzas (Para Variações)
```
#F5F5F5 - Fundo alternativo (hover, ligeiro)
#E0E0E0 - Bordas, divisores
#5F6C7B - Texto claro, hints
```

---

## 🎯 Componentes por Tipo

### 1. NAVEGAÇÃO
```
┌─────────────────────────────────┐
│ 🔐 Controle de Acesso [Botões▼]│
│ ├─ Monitoramento               │
│ ├─ Acessos Pessoais            │
│ ├─ Acessos Veiculares          │
│ ├─ Veículos                    │
│ ├─ Empresas                    │
│ ├─ Usuários                    │
│ └─ 👤 João Silva [Sair]        │
└─────────────────────────────────┘
Cor: Gradient verde #0B7A47 → #1B9456
Efeito: Hover com background transparente
```

### 2. CARDS
```
┌──────────────────────────────┐
│  Título Card                 │
│  Lorem ipsum dolor sit amet  │
│  consectetur adipiscing elit │
└──────────────────────────────┘
Shadow: Suave, elevação no hover
Border-radius: 12px
Padding: 24px
Hover: Shadow aumentado + -2px translateY
```

### 3. FORMULÁRIO
```
┌─────────────────────────┐
│ Nome do Campo *         │
│ [Input com borda verde] │
│                         │
│ CNPJ *                  │
│ [Input com borda verde] │
│                         │
│ [Botão Verde] [Cancelar]│
└─────────────────────────┘

Input Focus:
├─ Borda: 2px #0B7A47
├─ Shadow: 0 0 0 4px rgba(11, 122, 71, 0.1)
└─ Background: Branco puro
```

### 4. TABELAS
```
┌────────┬────────┬────────┬──────────┐
│ Nome   │ Email  │ Tipo   │ Ações    │ ← Header verde
├────────┼────────┼────────┼──────────┤
│ João   │ j@... │ Admin  │ [Ed] [Del]│
├────────┼────────┼────────┼──────────┤
│ Maria  │ m@... │ Oper   │ [Ed] [Del]│ ← Hover fundo verde claro
└────────┴────────┴────────┴──────────┘

Header: Gradient verde, texto branco
Linhas: Hover em #E8F5ED (verde muito claro)
Bordas: #E0E0E0 (cinza suave)
```

### 5. BOTÕES
```
PRIMÁRIO (Submit)
┌──────────────────┐
│  Salvar Usuário  │ ← Verde com shadow
└──────────────────┘
Hover: Escuro + elevação + shadow maior

SECUNDÁRIO (Cancel)
┌──────────────────┐
│    Cancelar      │ ← Cinza com borda
└──────────────────┘
Hover: Cinza mais escuro

PERIGO (Delete)
┌──────────────────┐
│     Deletar      │ ← Vermelho com shadow
└──────────────────┘
Hover: Vermelho escuro + elevação
```

---

## 🎬 Animações

### Hover Suave (Botões/Cards)
```
Estado Normal → Hover
├─ Transform: translateY(-2px)
├─ Shadow: aumenta
├─ Duração: 0.3s
└─ Easing: cubic-bezier(0.4, 0, 0.2, 1)
```

### Focus Input
```
Estado Normal → Focus
├─ Border-color: #0B7A47
├─ Box-shadow: 0 0 0 4px rgba(11, 122, 71, 0.1)
├─ Duração: 0.3s
└─ Sem "pulo" visual
```

### Modal/Dialog
```
Entrada:
├─ Fade-in: 0.3s
├─ Slide-up: 30px → 0px
└─ Easing: cubic-bezier(0.4, 0, 0.2, 1)
```

---

## 📱 Responsividade em Ação

### Desktop (1024px+)
```
Formulário:
┌──────────┬──────────┐
│ Campo 1  │ Campo 2  │
├──────────┼──────────┤
│ Campo 3  │ Campo 4  │
└──────────┴──────────┘

Tabela:
┌──────┬──────┬──────┬──────┐
│ Col1 │ Col2 │ Col3 │ Col4 │
└──────┴──────┴──────┴──────┘
```

### Tablet (768px)
```
Formulário:
┌──────────────────┐
│ Campo 1 │ Campo2 │
├────────┬────────┤
│ Campo 3│ Campo4 │
└────────┴────────┘

Tabela: Começa a adaptar
```

### Mobile (<768px)
```
Formulário:
┌──────────────┐
│ Campo 1      │
├──────────────┤
│ Campo 2      │
├──────────────┤
│ Campo 3      │
└──────────────┘

Tabela (Card Style):
┌─────────────────┐
│ 🏷️ Nome: João   │
│ 📧 Email: j@... │
│ 🔖 Tipo: Admin  │
│ [Editar] [Del]  │
├─────────────────┤
│ 🏷️ Nome: Maria  │
│ 📧 Email: m@... │
│ 🔖 Tipo: Oper   │
│ [Editar] [Del]  │
└─────────────────┘

Navbar: Stack Vertical
┌─────────────────┐
│ 🔐 Controle     │
├─────────────────┤
│ Monitoramento   │
│ Acessos Pessoal │
│ Acessos Veicular│
│ Veículos        │
│ Empresas        │
│ Usuários        │
│ 👤 João [Sair]  │
└─────────────────┘
```

---

## 🎨 Exemplos de Gradientes

### Navbar / Botão Primário
```css
linear-gradient(135deg, #0B7A47 0%, #1B9456 100%)
```
Ângulo: 135° (topo-esquerda para baixo-direita)

### Hover Botão Primário
```css
linear-gradient(135deg, #055A35 0%, #0B7A47 100%)
```
Mais escuro para efeito de profundidade

---

## 🔍 Detalhes de Espaçamento

### Padding Interno
```
Inputs: 10px 12px
Buttons: 11px 20px
Cards: 24px
Navbar: 70px height
```

### Gaps entre Elementos
```
Formulário: 20px
Botões: 12px
Itens Menu: 5px
```

### Margin Externo
```
Containers: 30px auto
Cards: margin-bottom 20px
Titles: margin-bottom 30px
```

---

## ✨ Shadows por Profundidade

### Shadow SM (Leve)
```
0 2px 8px rgba(11, 122, 71, 0.08)
Uso: Cards, inputs, botões padrão
```

### Shadow MD (Médio)
```
0 4px 12px rgba(11, 122, 71, 0.12)
Uso: Cards principais, formulários
```

### Shadow LG (Grande)
```
0 8px 24px rgba(11, 122, 71, 0.15)
Uso: Modals, dropdowns, hover cards
```

---

## 🎯 Checklist de Design

- ✅ Cores: Verde #0B7A47 como primário
- ✅ Fundo: Branco puro ou gradient suave
- ✅ Bordas: 2px em inputs, #E0E0E0 em tabelas
- ✅ Border-radius: 8px (inputs), 12px (cards)
- ✅ Shadows: Com cor verde, não preto
- ✅ Hover: Elevação -2px + shadow aumentado
- ✅ Transições: cubic-bezier smooth 0.3s
- ✅ Typography: System fonts, pesos 400/500/600/700
- ✅ Responsividade: Mobile-first, testar até 320px
- ✅ Acessibilidade: Contraste WCAA AA+

---

## 🎬 Visualização

Abra: **http://localhost:5174**

Veja em ação:
1. 🌐 Navegação verde moderna
2. 📋 Tabelas com hover effect
3. 📝 Formulários com focus state
4. 🎨 Cards com shadows suaves
5. 📱 Totalmente responsivo
6. ✨ Animações fluidas

---

**Design System**: TERCEIRIZE+
**Versão**: 1.0
**Status**: ✅ Pronto para Produção
**Data**: 27/11/2025
