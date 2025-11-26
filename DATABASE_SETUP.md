# 🗄️ Guia de Configuração do Banco de Dados

## 📋 Pré-requisitos

Antes de executar a aplicação, você precisa:

1. **MySQL/MariaDB instalado** no seu sistema
2. **Porta 3307 acessível** (padrão do MySQL)
3. **Credenciais corretas** no arquivo `.env`

## ⚙️ Passo 1: Iniciar o Serviço MySQL/MariaDB

### No Windows (via PowerShell como Administrador)

```powershell
# Para MariaDB
net start mariadb

# Para MySQL
net start MySQL80
# ou
net start "MySQL80" # Se houver espaços no nome
```

### Verificar se o serviço está rodando

```powershell
Get-Service | Where-Object {$_.Name -like "*mysql*" -or $_.Name -like "*maria*"}
```

### Se não conseguir iniciar via net start

```powershell
# Via sc (Service Control)
sc start MySQL80

# Ou reinstale o serviço
mysqld --install
mysqld --start
```

## 📝 Passo 2: Configurar o Arquivo .env

Crie ou atualize o arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=mysql+pymysql://root:sua_senha@localhost:3307/controle_acesso
SECRET_KEY=sua_chave_secreta_muito_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Configurações explicadas:

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `DATABASE_URL` | String de conexão com MySQL | `mysql+pymysql://root:senha@localhost:3307/controle_acesso` |
| `SECRET_KEY` | Chave para assinar tokens JWT | `sua_chave_super_segura_123` |
| `ALGORITHM` | Algoritmo de assinatura JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração do token | `30` |

## 🗄️ Passo 3: Criar o Banco de Dados

### Opção A: Via MySQL CLI (Recomendado)

```bash
# Conectar ao MySQL
mysql -u root -p

# No prompt MySQL, execute:
CREATE DATABASE controle_acesso CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Verificar criação
SHOW DATABASES;

# Sair
EXIT;
```

### Opção B: Via Python Script

```python
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sua_senha"
)

cursor = conn.cursor()
cursor.execute("CREATE DATABASE controle_acesso CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
print("Banco de dados criado com sucesso!")
cursor.close()
conn.close()
```

## 📊 Passo 4: Executar os Scripts SQL

Execute os scripts de criação de tabelas **nesta ordem**:

### Script 1: Query 1.sql
```bash
mysql -u root -p controle_acesso < "querys/Query 1.sql"
```

### Script 2: Query 2.sql
```bash
mysql -u root -p controle_acesso < "querys/Query 2.sql"
```

### Script 3: Query 3.sql (Opcional - Seeds/Dados de Teste)
```bash
mysql -u root -p controle_acesso < "querys/Query 3.sql"
```

## ✅ Passo 5: Verificar a Conexão

### Teste 1: Via MySQL CLI
```bash
mysql -u root -p controle_acesso -e "SHOW TABLES;"
```

Você deve ver as tabelas criadas:
- `usuarios`
- `veiculos`
- `acessos_pessoais`
- `acessos_veiculares`
- E outras conforme seus scripts

### Teste 2: Via Python
```python
from app.database.connection import engine

try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("✅ Conexão com banco de dados bem-sucedida!")
except Exception as e:
    print(f"❌ Erro na conexão: {e}")
```

## 🚀 Passo 6: Iniciar a Aplicação

### Via run.py
```bash
python run.py
```

Você deve ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

### Via Uvicorn direto
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🧪 Passo 7: Testar os Endpoints

### Via Script de Testes
```bash
python test_api.py
```

Você verá um relatório completo com status de todos os testes:
```
============================================================
INICIANDO TESTES DA API DE CONTROLE DE ACESSO
============================================================
✅ Servidor conectado com sucesso!
✅ Testando conexão com banco de dados...

============================================================
COMEÇANDO TESTES DOS ENDPOINTS
============================================================

✓ Testando Health Check...
[GET /health] 200 OK: {"status": "ok"}

✓ Testando Registrar Usuário...
[POST /usuarios/registro] 201 CREATED: {"id_usuario": 1, ...}

... mais testes ...

============================================================
RESUMO DOS TESTES
============================================================
Health Check: ✓ PASSOU
Registrar Usuário: ✓ PASSOU
Login: ✓ PASSOU
... resumo ...
Total: 11/11 testes passaram
============================================================
```

### Via cURL
```bash
# Health Check
curl http://localhost:8000/health

# Registrar Usuário
curl -X POST http://localhost:8000/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "documento": "12345678901",
    "login": "joao.silva",
    "senha": "senha123"
  }'

# Login
curl -X POST http://localhost:8000/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{
    "login": "joao.silva",
    "senha": "senha123"
  }'
```

### Via Swagger UI (Recomendado)
Abra seu navegador e acesse:
```
http://localhost:8000/docs
```

Você terá uma interface interativa para testar todos os endpoints!

## 🔧 Troubleshooting

### ❌ "Can't connect to MySQL server on 'localhost' (port 3307)"

**Solução:**
```bash
# Verificar se o serviço está rodando
Get-Service | Where-Object {$_.Name -like "*mysql*"}

# Iniciar o serviço
net start MySQL80

# Ou verificar a porta
netstat -ano | findstr :3307
```

### ❌ "Access denied for user 'root'@'localhost'"

**Solução:**
1. Verifique a senha no arquivo `.env`
2. Redefinir senha MySQL:
```bash
# Parar MySQL
net stop MySQL80

# Reiniciar sem autenticação
mysqld --skip-grant-tables

# Em outro terminal, conectar sem senha
mysql -u root

# Redefinir senha
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'nova_senha';
EXIT;

# Parar o serviço e reiniciar normalmente
```

### ❌ "database controle_acesso does not exist"

**Solução:**
```bash
# Criar o banco de dados
mysql -u root -p -e "CREATE DATABASE controle_acesso CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Executar os scripts SQL
mysql -u root -p controle_acesso < "querys/Query 1.sql"
```

### ❌ "JSONDecodeError" durante testes

**Isto significa:** O servidor respondeu com erro (HTTP 500) e o JSON é inválido.

**Solução:**
1. Verifique se MySQL está rodando
2. Verifique os logs do servidor (console onde executou `run.py`)
3. Certifique-se que as tabelas foram criadas corretamente

### ❌ Erro ao executar scripts SQL

**Solução:**
```bash
# Ver mais detalhes do erro
mysql -u root -p controle_acesso < "querys/Query 1.sql" 2>&1

# Executar manualmente
mysql -u root -p controle_acesso

# No prompt MySQL, copie o conteúdo do arquivo SQL e execute linha por linha
```

## 📚 Estrutura do Banco de Dados

### Tabelas Principais

```
usuarios
├── id_usuario (PK)
├── nome
├── documento (UNIQUE)
├── login (UNIQUE)
├── senha_hash
├── ativo
└── data_cadastro

veiculos
├── id_veiculo (PK)
├── placa (UNIQUE)
├── modelo
├── ano
└── id_responsavel (FK → usuarios)

acessos_pessoais
├── id_acesso (PK)
├── id_usuario (FK → usuarios)
├── hora_entrada
├── hora_saida
├── motivo_visita
└── observacao

acessos_veiculares
├── id_acesso_veiculo (PK)
├── id_veiculo (FK → veiculos)
├── id_responsavel (FK → usuarios)
├── hora_entrada
├── hora_saida
└── observacao
```

## 🔑 Credenciais Padrão (Se aplicável)

Se seus scripts SQL criam dados de teste, use:

```json
{
  "login": "admin",
  "senha": "admin123"
}
```

*Mude estas credenciais em produção!*

## ✨ Próximos Passos

1. ✅ Banco de dados rodando
2. ✅ Aplicação iniciada
3. ✅ Testes passando
4. 📖 Leia `GUIDE.md` para detalhes dos endpoints
5. 🏗️ Leia `ARCHITECTURE.md` para entender a estrutura do código
6. 🚀 Implemente suas regras de negócio!

---

**Suporte:** Se ainda tiver dúvidas, verifique `PROJECT_STATUS.md` para o status atual do projeto.
