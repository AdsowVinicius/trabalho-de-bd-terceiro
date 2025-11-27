# Guia de Acesso - Perfis Autorizados

A aplicação agora permite acesso para 4 perfis diferentes:

## Perfis Autorizados
1. **Porteiro** (ID: 1)
2. **Funcionário** (ID: 2)  
3. **Administrador** (ID: 3)
4. **Segurança** (ID: 4)

## Usuários de Teste Criados

### Porteiro
- **Login**: `porteiro_teste`
- **Senha**: `senha123`

### Funcionário
- **Login**: `funcionario_teste`
- **Senha**: `senha123`

### Administrador
- **Login**: `admin_teste`
- **Senha**: `senha123`

### Segurança
- **Login**: `seguranca_teste`
- **Senha**: `senha123`

## Usuário Admin Existente
- **Login**: `admin`
- **Senha**: `admin`

## Testando

1. Acesse a aplicação em `http://localhost:5174`
2. Use qualquer uma das credenciais acima para fazer login
3. Você será redirecionado para a página de "Acessos Pessoais"
4. Todos os perfis têm acesso total ao painel

## Alterações Realizadas

### Backend
- ✓ Atualizado `app/utils/security.py` para lidar com hashes inválidos
- ✓ Perfis de acesso atualizados na tabela `lu_perfis_acesso`
- ✓ Endpoint de lookups dinâmico para detectar colunas automaticamente

### Frontend
- ✓ Página de login permite acesso para: Porteiro, Funcionário, Administrador e Segurança
- ✓ Mensagem informativa atualizada
- ✓ Validação de perfis dinâmica

## Observações

- A página de login verifica o perfil do usuário após a autenticação
- Apenas usuários com os perfis autorizados conseguem acessar o painel
- O JWT token é salvo no localStorage para futuros acessos
- As informações do usuário também são salvas no localStorage
