# 🔧 COMO REPRODUZIR - ACESSOS VEICULARES

## Repositorio Atual

```
c:\Users\adsow\Desktop\trabalho de bd terceiro\
```

---

## Passo 1: Verificar Backend Rodando

### Terminal PowerShell
```powershell
cd 'c:\Users\adsow\Desktop\trabalho de bd terceiro'
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

### Esperado
```
Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
Application startup complete
```

---

## Passo 2: Verificar Frontend Rodando

### Outro Terminal PowerShell
```powershell
cd 'c:\Users\adsow\Desktop\trabalho de bd terceiro\frontend'
npm run dev
```

### Esperado
```
VITE v4.x.x  ready in xxx ms

Local:     http://localhost:5174/
```

---

## Passo 3: Acessar Aplicacao

### URL
```
http://localhost:5174
```

### Você verá
- Pagina de Login com campo usuario/senha
- Opcoes de perfil (Porteiro, Funcionario, Administrador, Seguranca)

---

## Passo 4: Login

### Credenciais Teste (Porteiro)
```
Usuario: porteiro_teste
Senha: senha123
```

### Outras Opcoes
```
usuario: funcionario_teste, senha: senha123
usuario: admin_teste, senha: senha123
usuario: seguranca_teste, senha: senha123
usuario: joao_silva, senha: senha123
```

---

## Passo 5: Acessar Formulario de Acessos Veiculares

### Menu Principal
Apos login, clique em: **"Acessos Veiculares"**

### URL Direta
```
http://localhost:5174/acessos-veiculares
```

---

## Passo 6: Testar Formulario

### Campo 1: Pesquisar Veiculo
1. Clique no campo "Pesquisar Veiculo"
2. Digite: `ABC`
3. Espere dropdown aparecer
4. Clique em: `ABC-1234 - Fiat Uno (2020)`
5. Veraque auto-preenchimento:
   - Placa: ABC-1234
   - Ano: 2020
   - Modelo: Fiat Uno

### Campo 2: Pesquisar Responsavel
1. Clique no campo "Pesquisar Responsavel"
2. Digite: `João`
3. Espere dropdown aparecer
4. Clique em: `João Silva (12345678900) - joao_silva`
5. Verifique que id_responsavel foi definido

### Campo 3: Tipo de Servico
1. Select ja tem valor padrao
2. Pode clicar para escolher outro tipo (se houver)

### Campo 4: Nota Fiscal Entrada (opcional)
1. Clique no campo
2. Digite: `NF-123456`

### Campo 5: Nota Fiscal Saida (opcional)
1. Deixe em branco (ou digite outro)

### Campo 6: Pesquisar Transportadora (opcional)
1. Clique no campo "Pesquisar Transportadora"
2. Digite: `Empresa`
3. Espere dropdown aparecer
4. Clique em: `Empresa Exemplo`

### Campo 7: Observacao (opcional)
1. Clique no campo textarea
2. Digite: `Teste de acesso veicular`

### Passo 7: Registrar
1. Clique no botao: **"Registrar Acesso Veicular"**
2. Espere mensagem de sucesso
3. Formulario sera limpo

---

## Verificar No Banco de Dados

### Abrir MySQL Workbench ou Adminer

```sql
-- Conectar a:
Host: 127.0.0.1
Port: 3307
User: root
Password: admin
Database: controle_acesso

-- Query para verificar registro:
SELECT * FROM acessos_veiculares ORDER BY id_acesso_veicular DESC LIMIT 1;
```

### Resultado Esperado
```
id_acesso_veicular: (incrementado automaticamente)
id_veiculo: 2
id_responsavel: 3
id_tipo_servico: 1
nota_fiscal_entrada: NF-123456
nota_fiscal_saida: NULL
id_transportadora: 1
hora_entrada: 2025-11-27 HH:MM:SS
hora_saida: NULL
observacao: Teste de acesso veicular
data_registro: 2025-11-27
```

---

## Testar Endpoints Diretamente

### PowerShell / Python
```python
import requests
import json

# 1. Login
login = requests.post('http://127.0.0.1:8001/usuarios/login', 
    json={'login': 'porteiro_teste', 'senha': 'senha123'})
token = login.json()['access_token']
print(f"Token: {token[:20]}...")

# 2. Testar lookup de veiculos
veiculos = requests.get('http://127.0.0.1:8001/lookups/veiculos')
print(f"Veiculos: {veiculos.json()}")

# 3. Testar lookup de responsaveis
responsaveis = requests.get('http://127.0.0.1:8001/lookups/responsaveis')
print(f"Responsaveis: {len(responsaveis.json())} encontrados")

# 4. Testar lookup de transportadoras
transportadoras = requests.get('http://127.0.0.1:8001/lookups/transportadoras')
print(f"Transportadoras: {transportadoras.json()}")

# 5. Testar POST
acesso = requests.post('http://127.0.0.1:8001/acessos-veiculares/',
    json={
        "id_veiculo": 2,
        "id_responsavel": 3,
        "id_tipo_servico": 1,
        "nota_fiscal_entrada": "NF-999999",
        "id_transportadora": 1,
        "observacao": "Teste via API"
    },
    headers={'Authorization': f'Bearer {token}'}
)
print(f"POST Status: {acesso.status_code}")
print(f"Resultado: {acesso.json()}")
```

---

## Troubleshooting

### ❌ Dropdown nao aparece
**Solucao:**
1. Verifique se endpoint GET /lookups/XXXX retorna dados
2. Veja console (F12 > Console) para erros JavaScript
3. Reinicie o frontend

### ❌ Auto-preenchimento nao funciona
**Solucao:**
1. Verifique que `selecionarVeiculo()` esta sendo chamada
2. Veja se o veiculo tem campos placa, ano, modelo no banco
3. Veja console para erros

### ❌ Botao de Registrar desabilitado
**Solucao:**
1. Certifique que VEICULO foi selecionado (nao digitado manualmente)
2. Certifique que RESPONSAVEL foi selecionado (nao digitado manualmente)
3. Verifique states no React DevTools (F12 > Components)

### ❌ POST retorna erro 400
**Solucao:**
1. Veja mensagem de erro na response
2. Verifique que id_veiculo existe no banco
3. Verifique que id_responsavel existe no banco
4. Verifique que id_tipo_servico existe no banco

### ❌ Erro de conexao ao banco
**Solucao:**
1. Inicie XAMPP Control Panel
2. Inicie MySQL
3. Verifique credenciais em `app/database/config.py`
4. Verifique se porta 3307 esta sendo usada

---

## Arquivos Importantes

### Frontend
```
frontend/src/pages/AcessoVeicular.jsx    ← Componente principal
frontend/src/api.js                       ← Cliente HTTP
frontend/src/styles.css                   ← Estilos
```

### Backend
```
app/routes/lookups_routes.py             ← Endpoints GET
app/routes/acesso_veicular_routes.py     ← Endpoint POST
app/services/acesso_veicular_service.py  ← Logica
app/schemas/acesso_veicular_schema.py    ← Validacao
```

### Banco
```
Database: controle_acesso
Tables: usuarios, veiculos, acessos_veiculares, empresas
```

---

## Checklist de Verificacao

- [ ] Backend rodando na porta 8001
- [ ] Frontend rodando na porta 5174
- [ ] MySQL/Mariadb rodando na porta 3307
- [ ] Database "controle_acesso" existe
- [ ] Tabela "acessos_veiculares" existe
- [ ] Tabela "veiculos" tem dados
- [ ] Tabela "usuarios" tem dados
- [ ] Tabela "empresas" tem dados
- [ ] GET /lookups/veiculos retorna 200
- [ ] GET /lookups/responsaveis retorna 200
- [ ] GET /lookups/transportadoras retorna 200
- [ ] Login funciona com porteiro_teste
- [ ] Formulario carrega sem erros
- [ ] Dropdown funciona ao digitar
- [ ] Auto-preenchimento funciona
- [ ] POST cria registro no banco

---

## Como Resetar Tudo

### Limpar formulario
```javascript
// No browser console:
localStorage.clear()
location.reload()
```

### Resetar dados do banco
```sql
-- Deletar todos os acessos veiculares
DELETE FROM acessos_veiculares;

-- Resetar auto_increment
ALTER TABLE acessos_veiculares AUTO_INCREMENT = 1;
```

### Resetar estado da aplicacao
1. Feche o navegador
2. Limpe cache: Ctrl+Shift+Delete
3. Reabra a aplicacao

---

## Documentacao Adicional

Para mais detalhes, veja:

1. **ACESSOS_VEICULARES_NOVO.md** - Documentacao completa dos campos
2. **ACESSOS_VEICULARES_GUIA_RAPIDO.md** - Guia pratico passo-a-passo
3. **ACESSOS_VEICULARES_IMPLEMENTACAO.md** - Detalhes tecnicos
4. **ACESSOS_VEICULARES_RESUMO.md** - Resumo visual das mudancas
5. **FINAL_STATUS.md** - Status geral do projeto

---

## Support

Se tiver problemas:

1. Veja console do navegador (F12)
2. Veja logs do servidor FastAPI
3. Veja logs do MySQL
4. Veja arquivos de documentacao acima
5. Verifique credenciais do banco
6. Verifique que portas estao disponiveis

---

**Sucesso!** 🎉

Agora voce tem um formulario profissional de acessos veiculares funcionando.
