# 🎨 Design System Modernizado - TERCEIRIZE+

## Paleta de Cores

### Verde (Primary)
- **Verde Principal**: `#0B7A47` - Cor primária, inspirada no logo TERCEIRIZE+
- **Verde Escuro**: `#055A35` - Para hover e estados ativos
- **Verde Claro**: `#1B9456` - Para gradientes e destaques
- **Verde Muito Claro**: `#E8F5ED` - Para fundos de cards e highlights

### Neutros
- **Branco**: `#FFFFFF` - Fundo principal
- **Cinza Claro**: `#F5F5F5` - Fundos alternativos
- **Cinza Médio**: `#E0E0E0` - Bordas e divisores
- **Cinza Escuro**: `#9E9E9E` - Elementos desabilitados

### Texto
- **Texto Principal**: `#2C3E50` - Texto em corpos de texto
- **Texto Claro**: `#5F6C7B` - Texto secundário e hints

### Estados
- **Sucesso**: `#0B7A47` - Verde (mesmo da cor primária)
- **Perigo**: `#E74C3C` - Vermelho para ações destrutivas
- **Aviso**: `#F39C12` - Laranja para avisos
- **Info**: `#3498DB` - Azul para informações

---

## Componentes Atualizados

### 1. **Navegação (Nav.jsx)** ✅
- Gradient verde from `#0B7A47` to `#1B9456`
- Links com hover state com fundo transparente
- Logout button com estilo neutro
- Layout responsivo para mobile/tablet

### 2. **Formulários** ✅
- Inputs e selects com borda 2px em cinza
- Focus com borda verde + shadow suave
- Labels em preto com peso 600
- Padding aumentado (10px 12px)
- Border-radius de 8px (mais moderno)

### 3. **Botões** ✅
- **Primário**: Gradient verde com shadow
- **Secundário**: Cinza com borda
- **Perigo**: Vermelho para delete/logout
- Hover com `translateY(-2px)` para efeito de elevação
- Transitions smooth com cubic-bezier

### 4. **Tabelas** ✅
- Header com gradient verde
- Texto branco no header
- Linhas com hover em verde muito claro
- Card-style layout no mobile
- Shadow suave nas laterais

### 5. **Cards** ✅
- Fundo branco com shadow
- Border-radius 12px
- Padding 24px
- Hover com shadow aumentado + translateY(-2px)

### 6. **Avisos** ✅
- Success: Fundo verde claro + texto verde
- Error: Fundo vermelho claro + texto vermelho
- Warning: Fundo laranja claro + texto laranja

---

## Efeitos e Animações

### Transitions
```css
--transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

### Shadows
- **Shadow SM**: `0 2px 8px rgba(11, 122, 71, 0.08)`
- **Shadow MD**: `0 4px 12px rgba(11, 122, 71, 0.12)`
- **Shadow LG**: `0 8px 24px rgba(11, 122, 71, 0.15)`

### Hover Effects
- Botões: Elevação com `translateY(-2px)`
- Cards: Aumento de shadow + elevação
- Links: Background transparente no hover

### Animações
- **Spin**: Para loaders (360deg em 0.8s)
- **FadeIn**: Para modals (0.3s)
- **SlideUp**: Para modals (0.3s com cubic-bezier)

---

## Typography

- **Font Family**: System fonts (SF Pro Display, -apple-system, etc)
- **H1**: 36px, 700, letter-spacing -0.5px
- **H2**: 28px, 700, letter-spacing -0.3px
- **H3**: 20px, 600
- **Body**: 14px, 400, line-height 1.6
- **Small**: 12px, 400, line-height 1.5

---

## Responsividade

### Breakpoints
- **Mobile**: até 480px
- **Tablet**: 480px - 768px
- **Desktop**: 768px - 1024px
- **Wide**: 1024px+

### Comportamentos
- Formulários: 1 coluna em mobile, 2+ colunas em desktop
- Tabelas: Card-style layout em mobile
- Navbar: Stack vertical em mobile
- Padding reduzido em mobile

---

## Arquivo de Tema

Criado `theme.js` com:
- Constantes de cores
- Valores de shadow
- Transições padrão
- Border-radius presets
- Typography scale
- Gradientes pré-definidos
- Funções utilitárias para estilos dinâmicos

### Uso
```javascript
import { colors, shadows, transitions } from './theme'

const myStyles = {
  background: colors.primary,
  boxShadow: shadows.md,
  transition: transitions.default
}
```

---

## Classe CSS Principais

### Containers
- `.container` - Max-width 1200px com padding
- `.card` - Card com shadow e hover
- `.empty-state` - Estado vazio

### Formulários
- `.form-group` - Wrapper de campo
- `.form-error` - Mensagem de erro (vermelho)
- `.form-hint` - Hint/dica (cinza claro)
- `label` - Labels com estilo

### Botões
- `.btn-submit` - Botão primário (submit)
- `.btn-cancel` - Botão secundário (cancel)
- `.filter-button` - Botão de filtro
- `.btn-editar` / `.btn-excluir` - Ações de tabela

### Estados
- `.success-message` - Mensagem de sucesso
- `.error-message` - Mensagem de erro
- `.badge` - Badges (primary, success, danger, warning)
- `.loading` - Spinner loading

### Navegação
- `.navbar` - Navbar com gradient
- `.tabs` - Abas/tabs
- `.tab` - Tab individual com estados

---

## Gradientes Utilizados

### Primary
```css
linear-gradient(135deg, #0B7A47 0%, #1B9456 100%)
```

### Primary Dark
```css
linear-gradient(135deg, #055A35 0%, #0B7A47 100%)
```

---

## Melhorias Implementadas

✅ **Design Moderno**
- Cores em harmonia com TERCEIRIZE+ (branco + verde)
- Shadows suaves e naturais
- Border-radius consistente (8px e 12px)

✅ **Fluidez**
- Transitions smooth com cubic-bezier
- Hover effects com elevação
- Animações de entrada suaves

✅ **Acessibilidade**
- Contraste alto (preto on branco, branco on verde)
- Focus states bem definidos
- Fontes legíveis com line-height adequado

✅ **Responsividade**
- Mobile-first approach
- Breakpoints bem definidos
- Componentes adaptáveis

✅ **Consistência**
- Sistema de cores centralizado
- Espaçamento consistente
- Typography scale definida

---

## Como Usar

1. **Importar tema (opcional)**:
```javascript
import theme from './theme'
```

2. **Usar classes CSS** (recomendado):
```jsx
<div className="card">
  <h3>Título</h3>
  <p>Conteúdo</p>
</div>
```

3. **Usar variáveis CSS**:
```css
.meu-elemento {
  color: var(--color-primary);
  box-shadow: var(--shadow-md);
  transition: var(--transition);
}
```

---

## Status

🎨 **Design System**: ✅ Completo
🎭 **Componentes**: ✅ Modernizados (Nav, FormField, App)
📱 **Responsividade**: ✅ Testada
🎯 **Cores**: ✅ Alinhadas com TERCEIRIZE+
✨ **Efeitos**: ✅ Fluidos e modernos

**Data**: 27/11/2025
**Versão**: 1.0
