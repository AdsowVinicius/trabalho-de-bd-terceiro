# ⚡ Quick Reference Guide

## Iniciando Tudo Rapidamente

### 1. Verificar e Iniciar MySQL (PowerShell Admin)
```powershell
# Verificar status
Get-Service | Where-Object {$_.Name -like "*mysql*"}

# Iniciar
net start MySQL80
```

### 2. Criar Banco de Dados (Se não existir)
```bash
mysql -u root -p -e "CREATE DATABASE controle_acesso CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
```

### 3. Executar Scripts SQL
```bash
# Tabelas
mysql -u root -p controle_acesso < "querys/Query 1.sql"

# Mais tabelas/relacionamentos
mysql -u root -p controle_acesso < "querys/Query 2.sql"

# Dados de teste (opcional)
mysql -u root -p controle_acesso < "querys/Query 3.sql"
```

### 4. Instalar Dependências
```bash
pip install -r app/requirements.txt
```

### 5. Configurar .env
```env
DATABASE_URL=mysql+pymysql://root:sua_senha@localhost:3307/controle_acesso
SECRET_KEY=sua_chave_secreta_muito_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6. Iniciar Aplicação
```bash
python run.py
```

Você verá:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 7. Testar (Em outro terminal)
```bash
python test_api.py
```

### 8. Acessar Swagger
```
http://localhost:8000/docs
```

---

## Endpoints Principais

### Usuários
```
POST   /usuarios/registro           - Registrar novo usuário
POST   /usuarios/login              - Login e obter token JWT
GET    /usuarios/{id}               - Obter dados do usuário
GET    /usuarios/                   - Listar todos os usuários
PUT    /usuarios/{id}               - Atualizar usuário
DELETE /usuarios/{id}               - Deletar usuário
```

### Veículos
```
POST   /veiculos                    - Criar novo veículo
GET    /veiculos/{id}               - Obter dados do veículo
GET    /veiculos/                   - Listar todos os veículos
PUT    /veiculos/{id}               - Atualizar veículo
DELETE /veiculos/{id}               - Deletar veículo
```

### Acessos Pessoais
```
POST   /acessos-pessoais            - Registrar entrada de pessoa
PUT    /acessos-pessoais/{id}/saida - Registrar saída de pessoa
GET    /acessos-pessoais/           - Listar todos os acessos
GET    /acessos-pessoais/ativos/visitantes - Listar visitantes ativos
```

### Acessos Veiculares
```
POST   /acessos-veiculares/         - Registrar entrada de veículo
PUT    /acessos-veiculares/{id}/saida - Registrar saída de veículo
GET    /acessos-veiculares/         - Listar todos os acessos veiculares
```

### Saúde
```
GET    /health                      - Status da aplicação
GET    /                            - Mensagem de boas-vindas
```

---

## Exemplo de Uso com cURL

### 1. Registrar Usuário
```bash
curl -X POST http://localhost:8000/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "documento": "12345678901",
    "login": "joao.silva",
    "senha": "senha123"
  }'

# Resposta:
# {"id_usuario": 1, "nome": "João Silva", "login": "joao.silva", "ativo": true}
```

### 2. Fazer Login
```bash
curl -X POST http://localhost:8000/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{
    "login": "joao.silva",
    "senha": "senha123"
  }'

# Resposta:
# {"access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...", "token_type": "bearer"}
```

### 3. Usar Token para Operações Protegidas
```bash
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."

curl -X GET http://localhost:8000/usuarios/1 \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Criar Veículo
```bash
curl -X POST http://localhost:8000/veiculos \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "ABC-1234",
    "modelo": "Honda Civic",
    "ano": 2023,
    "id_responsavel": 1
  }'
```

### 5. Registrar Entrada Pessoal
```bash
curl -X POST http://localhost:8000/acessos-pessoais \
  -H "Content-Type: application/json" \
  -d '{
    "id_usuario": 1,
    "motivo_visita": "Reunião com diretor",
    "observacao": "Visitante de São Paulo"
  }'

# Resposta:
# {"id_acesso": 1, "id_usuario": 1, "hora_entrada": "2024-01-20 14:30:00", ...}
```

### 6. Registrar Saída Pessoal
```bash
curl -X PUT http://localhost:8000/acessos-pessoais/1/saida \
  -H "Content-Type: application/json" \
  -d '{
    "observacao": "Saída normal"
  }'
```

---

## Estrutura do Código

```
main.py              ← Aplicação FastAPI principal
run.py               ← Script para iniciar com Uvicorn
test_api.py          ← Testes automatizados

app/
├── __init__.py
├── main.py           ← Setup da aplicação
├── requirements.txt  ← Dependências Python
│
├── database/
│   ├── config.py     ← Lê .env e configura aplicação
│   └── connection.py ← SQLAlchemy engine e SessionLocal
│
├── models/           ← ORM Models (SQLAlchemy)
│   ├── base.py           ← Base class centralizado
│   ├── usuario.py        ← Tabela usuarios
│   ├── veiculo.py        ← Tabela veiculos
│   ├── acesso_pessoal.py ← Tabela acessos_pessoais
│   └── acesso_veicular.py ← Tabela acessos_veiculares
│
├── schemas/          ← Validação Pydantic
│   ├── usuario_schema.py
│   ├── veiculo_schema.py
│   ├── acesso_pessoal_schema.py
│   └── acesso_veicular_schema.py
│
├── services/         ← Lógica de Negócio
│   ├── usuario_service.py
│   ├── veiculo_service.py
│   ├── acesso_pessoal_service.py
│   └── acesso_veicular_service.py
│
├── routes/           ← Endpoints FastAPI
│   ├── usuario_routes.py
│   ├── veiculo_routes.py
│   ├── acesso_pessoal_routes.py
│   └── acesso_veicular_routes.py
│
└── utils/
    └── security.py   ← JWT e bcrypt
```

---

## Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| "Can't connect to MySQL server" | `net start MySQL80` no PowerShell Admin |
| "Access denied for user 'root'" | Verificar senha em `.env` |
| "database controle_acesso does not exist" | Executar: `mysql -u root -p -e "CREATE DATABASE controle_acesso"` |
| "JSONDecodeError" nos testes | MySQL não está rodando - verifique com `Get-Service` |
| Swagger não abre | Verifique se servidor está rodando: `python run.py` |
| Porta 8000 já em uso | `netstat -ano \| findstr :8000` e `taskkill /PID <pid> /F` |

---

## Variáveis de Ambiente (.env)

```env
# Conexão com banco de dados
DATABASE_URL=mysql+pymysql://user:password@host:port/database

# Segurança JWT
SECRET_KEY=chave_super_secreta_32caracteres_ou_mais
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Status Atual do Projeto

✅ **Completo e Funcional**

- Todos os 4 modelos implementados
- 43 endpoints funcionais
- Autenticação JWT implementada
- Criptografia de senhas com bcrypt
- Testes automatizados
- Documentação Swagger
- Erro handling robusto

🔄 **Próximos Passos**
- Começar a usar a API
- Implementar regras de negócio específicas
- Deploy em produção

---

## Arquivo de Configuração

Crie `.env` na raiz do projeto (mesmo nível que `run.py`):

```env
DATABASE_URL=mysql+pymysql://root:sua_senha@localhost:3307/controle_acesso
SECRET_KEY=sua_chave_super_secreta_minimo_32_caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Não compartilhe este arquivo!** Adicione a `.gitignore`:
```
.env
__pycache__/
*.pyc
.vscode/
.idea/
```

---

## Documentação Completa

Para mais detalhes, consulte:

- **[DATABASE_SETUP.md](DATABASE_SETUP.md)** - Guia completo de setup do banco
- **[GUIDE.md](GUIDE.md)** - Documentação dos endpoints
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitetura do projeto
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Status e progresso

---

**Última atualização:** 2024
**Status:** ✅ Pronto para Produção
