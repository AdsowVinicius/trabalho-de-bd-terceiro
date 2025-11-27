# 🔧 GUIA DE SETUP DO BANCO DE DADOS - RESOLUÇÃO DE PROBLEMAS

## ⚠️ Problemas Identificados

Se você está recebendo erros como:
- `"Access denied for user 'root'@'localhost'"` 
- `"Unknown database 'terceira_bd'"`
- `"Can't connect to MySQL server"`

Este guia vai resolver!

---

## 🚀 PASSO 1: Verificar Porta e Serviço MySQL

### Verificar se MySQL está rodando (Windows)

```powershell
# PowerShell como Administrador
Get-Service | Where-Object {$_.Name -like "*mysql*" -or $_.Name -like "*maria*"}

# Você deve ver algo como:
# Status   Name                DisplayName
# ------   ----                -----------
# Running  MySQL80             MySQL80
```

### Se não estiver rodando:

```powershell
# Iniciar MySQL
net start MySQL80

# Ou para MariaDB
net start MariaDB
```

### Descobrir qual porta MySQL está usando:

```bash
netstat -ano | findstr :3306
# ou
netstat -ano | findstr :3307
```

---

## 🚀 PASSO 2: Validar Credenciais

### Testar conectar ao MySQL via CLI:

```bash
# Conectar como root SEM senha
mysql -h 127.0.0.1 -u root

# Se funcionar, faça login com senha
mysql -h 127.0.0.1 -u root -p
# Digite a senha quando solicitado
```

### Se receber "Access denied":

1. **Redefinir senha do root:**

```bash
# Parar MySQL
net stop MySQL80

# Iniciar sem autenticação
mysqld --skip-grant-tables --bind-address=127.0.0.1

# Em outro terminal
mysql -u root

# Dentro do MySQL
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'admin';
EXIT;

# Parar MySQL
net stop MySQL80

# Reiniciar normalmente
net start MySQL80
```

2. **Verificar if root tem acesso local:**

```bash
mysql -u root -p

# Dentro do MySQL
SELECT user, host FROM mysql.user WHERE user='root';
```

---

## 🚀 PASSO 3: Descobrir Porta Correta

### Ver todas as portas MySQL em uso:

```bash
# PowerShell
netstat -ano | findstr "LISTEN" | findstr -E "(3306|3307|3308)"

# Resultado esperado:
# TCP    127.0.0.1:3306         0.0.0.0:0              LISTENING       1234
#       ^^^^^^^ Porta 3306 (padrão)
```

### Se MySQL estiver em porta diferente:

- **Porta 3306:** Padrão (use `127.0.0.1:3306`)
- **Porta 3307:** Secundária (use `127.0.0.1:3307`)
- **Porta 3308:** Terciária (use `127.0.0.1:3308`)

---

## 🔧 PASSO 4: Configurar .env Corretamente

### Edite o arquivo `.env` na raiz do projeto:

```env
# Teste qual porta está funcionando
# Tente 3306 primeiro
DATABASE_URL=mysql+pymysql://root:admin@127.0.0.1:3306/controle_acesso

# Se receber erro de porta, tente
# DATABASE_URL=mysql+pymysql://root:admin@127.0.0.1:3307/controle_acesso

SECRET_KEY=sua_chave_secreta_muito_segura_aqui_32_caracteres_minimo
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Formato do DATABASE_URL:

```
mysql+pymysql://[usuario]:[senha]@[host]:[porta]/[banco]
                 ^^^^^^    ^^^^^    ^^^^  ^^^^  ^^^^
                 root      admin    127.0.0.1  3306  controle_acesso
```

---

## 🗄️ PASSO 5: Criar Banco de Dados

### Verificar bancos existentes:

```bash
mysql -u root -p -e "SHOW DATABASES;"
```

### Criar banco "controle_acesso":

```bash
# Via CLI
mysql -u root -p -e "CREATE DATABASE controle_acesso CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Ou via SQL direto
mysql -u root -p
# Dentro do MySQL:
CREATE DATABASE controle_acesso CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES;
EXIT;
```

---

## 📊 PASSO 6: Executar Scripts SQL

### Verificar se os scripts existem:

```powershell
# PowerShell
Get-ChildItem -Path ".\querys\" -Filter "*.sql"

# Você deve ver:
# Query 1.sql
# Query 2.sql
# Query 3.sql
```

### Executar em ordem:

```bash
# Script 1 - Tabelas principais
mysql -u root -p controle_acesso < "querys/Query 1.sql"

# Script 2 - Relacionamentos/Índices
mysql -u root -p controle_acesso < "querys/Query 2.sql"

# Script 3 - Dados de teste (opcional)
mysql -u root -p controle_acesso < "querys/Query 3.sql"
```

### Verificar tabelas criadas:

```bash
mysql -u root -p -e "USE controle_acesso; SHOW TABLES;"

# Você deve ver:
# +------------------------+
# | Tables_in_controle_acesso |
# +------------------------+
# | usuarios              |
# | veiculos              |
# | acessos_pessoais      |
# | acessos_veiculares    |
# +------------------------+
```

---

## 🧪 PASSO 7: Testar Conexão

### Via Python (diagnose_db.py):

```bash
python diagnose_db.py
```

**Resultado esperado:**
```
============================================================
DIAGNÓSTICO DE BANCO DE DADOS
============================================================
✅ MySQL está conectado com sucesso!

📊 Bancos de dados disponíveis:
   - information_schema
   - mysql
   - performance_schema
   - controle_acesso

✅ Banco 'controle_acesso' existe!

📋 Tabelas (4 encontradas):
   - usuarios
   - veiculos
   - acessos_pessoais
   - acessos_veiculares

============================================================
✅ Diagnóstico concluído!
============================================================
```

---

## 🚀 PASSO 8: Iniciar Aplicação

### Limpar cache Python:

```powershell
Get-ChildItem -Path . -Include __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force
```

### Rodar servidor:

```bash
python run.py
```

**Resultado esperado:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Em outro terminal, rodar testes:

```bash
python test_api.py
```

---

## 📋 Checklist de Troubleshooting

```
[ ] MySQL está rodando? (Get-Service)
[ ] Porta está correta? (netstat)
[ ] Credenciais são válidas? (mysql -u root -p)
[ ] Banco controle_acesso existe? (SHOW DATABASES)
[ ] Tabelas foram criadas? (SHOW TABLES)
[ ] .env tem DATABASE_URL correto?
[ ] .env tem SECRET_KEY preenchido?
[ ] PyCache foi limpo?
[ ] Servidor inicia sem erro?
[ ] Health check funciona? (GET /health)
```

---

## 🔍 Erros Comuns e Soluções

### Erro: "Access denied for user 'root'@'localhost' (using password: NO)"

**Causa:** Pydantic não está lendo .env corretamente

**Solução:**
1. Verifique se `case_sensitive = False` está em `app/database/config.py`
2. Limpe `__pycache__`: `Get-ChildItem -Path . -Include __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force`
3. Reinicie servidor

### Erro: "Unknown database 'terceira_bd'"

**Causa:** Database antigo ainda em memória cache

**Solução:**
1. Limpe cache Python
2. Verifique .env tem `controle_acesso` (não `terceira_bd`)
3. Reinicie servidor

### Erro: "Can't connect to MySQL server on 'localhost' (port 3306)"

**Causa:** MySQL não está rodando na porta 3306

**Solução:**
1. Verifique qual porta: `netstat -ano | findstr :3306`
2. Se porta diferente, edite DATABASE_URL em .env
3. Se MySQL não está rodando: `net start MySQL80`

### Erro: "ERROR 1045 (28000): Access denied for user 'root'@'localhost'"

**Causa:** Senha errada ou MySQL não reconhece usuário

**Solução:**
1. Teste manualmente: `mysql -u root -p`
2. Se falhar, redefinir senha (veja PASSO 2)
3. Após redefinir, atualize senha em .env

---

## ✅ Validação Final

Quando tudo está certo, você deve ver:

```bash
$ python test_api.py

============================================================
INICIANDO TESTES DA API DE CONTROLE DE ACESSO
============================================================
✅ Servidor FastAPI está rodando
✅ Testando conexão com banco de dados...

✓ Testando Health Check...
[GET] /health
Status: 200
Response: {
  "status": "ok",
  "servico": "Controle de Acesso"
}

✓ Testando Registro de Usuário...
[POST] /usuarios/registro
Status: 201
Response: {
  "id_usuario": 1,
  "nome": "João Silva",
  ...
}

... (mais testes)

============================================================
RESUMO DOS TESTES
============================================================
Health Check: ✓ PASSOU
Registrar Usuário: ✓ PASSOU
Login: ✓ PASSOU
... (11 testes)

Total: 11/11 testes passaram
============================================================
```

---

## 📞 Ainda com Problemas?

1. **Execute diagnose_db.py** e veja a saída
2. **Verifique os logs do servidor** na coluna "Last Command Output"
3. **Confira a mensagem de erro** exata que recebe
4. **Siga o PASSO 2** se erro for de autenticação
5. **Siga o PASSO 3** se erro for de porta
6. **Siga o PASSO 5** se erro for de banco não existir

---

**Você consegue! 💪 Qualquer dúvida, siga os passos na ordem exata.**

