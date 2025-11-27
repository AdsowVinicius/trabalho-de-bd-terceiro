# 🔐 RESOLVER PROBLEMA DE SENHA MYSQL

## Status Atual
- ✅ MySQL94 está rodando
- ❌ Conexão com root@localhost está FALHANDO
- ❌ A senha "admin" não é válida

---

## Opções para Resolver

### Opção 1: Testar Acesso sem Senha

```bash
# Tente conectar sem senha
mysql -h 127.0.0.1 -u root

# Se funcionar, a senha é vazia!
# Nesse caso, edite .env para:
# DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/controle_acesso
```

### Opção 2: Verificar Senha Padrão do MySQL

Dependendo de como instalou:

```bash
# Teste cada um desses:
mysql -u root -p"" -h 127.0.0.1              # Sem senha
mysql -u root -p"root" -h 127.0.0.1          # Senha = root
mysql -u root -p"password" -h 127.0.0.1      # Senha = password
mysql -u root -p"123456" -h 127.0.0.1        # Senha = 123456
mysql -u root -p"admin" -h 127.0.0.1         # Senha = admin
```

### Opção 3: Redefinir Senha do Root (Windows Admin)

**Pré-requisito: Executar PowerShell/CMD como Administrador**

```bash
# 1. Parar MySQL
net stop MySQL94

# 2. Iniciar sem autenticação
"C:\Program Files\MySQL\MySQL Server 9.4\bin\mysqld.exe" --skip-grant-tables --bind-address=127.0.0.1

# (deixe esse terminal aberto)
```

**Em OUTRO terminal (não admin):**

```bash
# 3. Conectar sem senha
mysql -u root -h 127.0.0.1

# 4. Dentro do MySQL, execute:
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'admin';
-- Ou escolha outra senha:
-- ALTER USER 'root'@'localhost' IDENTIFIED BY 'sua_nova_senha';

EXIT;
```

**Volte ao terminal admin:**

```bash
# 5. Ctrl+C para parar mysqld.exe

# 6. Reiniciar MySQL normalmente
net start MySQL94
```

### Opção 4: Usar Usuário Diferente

Se root não funcionar, talvez exista outro usuário:

```bash
# Conectar como "Usuario" comum
mysql -u usuario -p -h 127.0.0.1

# Ou verificar quem criou o BD
# Edite .env com as credenciais que conhece
```

---

## Próximo Passo

**Depois de escolher uma opção:**

1. Edite `.env` com a senha correta:

```env
# Se senha for vazia:
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/controle_acesso

# Se senha for "admin":
DATABASE_URL=mysql+pymysql://root:admin@127.0.0.1:3306/controle_acesso

# Se senha for outra:
DATABASE_URL=mysql+pymysql://root:sua_senha_aqui@127.0.0.1:3306/controle_acesso

SECRET_KEY=sua_chave_secreta_muito_segura_aqui_32_caracteres_minimo
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

2. Limpe cache Python:

```powershell
Get-ChildItem -Path . -Include __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force
```

3. Teste novamente:

```bash
python diagnose_db.py
```

---

## 💡 Dica Importante

Muitas vezes MySQL é instalado **sem senha padrão** para root.

Tente primeiro:

```bash
mysql -h 127.0.0.1 -u root
```

Se funcionar, use no .env:

```env
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/controle_acesso
```

(Note o `:@` - senha vazia entre os dois símbolos)

