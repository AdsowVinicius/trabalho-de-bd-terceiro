# 🚀 Guia de Inicialização e Uso

## Como Iniciar o Projeto

### 1. Instalação de Dependências

```bash
pip install -r requirements.txt
```

### 2. Configuração do Banco de Dados

#### Opção A: Se estiver usando MySQL/MariaDB

1. Execute o script SQL para criar o banco:
```bash
# Execute no seu cliente MySQL/MariaDB
mysql -u root -p < querys/Query\ 1.sql
mysql -u root -p < querys/Query\ 2.sql
```

2. Configure a conexão no arquivo `.env`:
```env
DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3307/controle_acesso
SECRET_KEY=sua-chave-secreta-muito-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Opção B: Criar arquivo `.env` com base no exemplo

```bash
copy .env.example .env
# Edite o .env com suas credenciais
```

### 3. Iniciar a Aplicação

#### Com reload automático (desenvolvimento):
```bash
python run.py
```

#### Ou diretamente:
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

A aplicação estará disponível em: **http://localhost:8000**

## Acessando a Documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testando os Endpoints

### 1️⃣ Registrar um novo usuário

```bash
curl -X POST "http://localhost:8000/usuarios/registro" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "documento": "12345678900",
    "id_tipo_usuario": 1,
    "login": "joao",
    "senha": "senha123",
    "id_perfil_acesso": 1,
    "contato": "11999999999"
  }'
```

### 2️⃣ Fazer login (obter token JWT)

```bash
curl -X POST "http://localhost:8000/usuarios/login" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "joao",
    "senha": "senha123"
  }'
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "usuario": {
    "id_usuario": 1,
    "nome": "João Silva",
    "documento": "12345678900",
    ...
  }
}
```

### 3️⃣ Registrar um veículo

```bash
curl -X POST "http://localhost:8000/veiculos/" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "ABC-1234",
    "modelo": "Fiat Uno",
    "ano": 2020,
    "id_responsavel": 1
  }'
```

### 4️⃣ Registrar entrada de pessoa

```bash
curl -X POST "http://localhost:8000/acessos-pessoais/" \
  -H "Content-Type: application/json" \
  -d '{
    "id_usuario": 1,
    "id_tipo_acesso": 1,
    "id_empresa_visitada": 1,
    "motivo_visita": "Reunião de trabalho"
  }'
```

### 5️⃣ Registrar saída de pessoa

```bash
curl -X PUT "http://localhost:8000/acessos-pessoais/1/saida" \
  -H "Content-Type: application/json" \
  -d '{
    "observacao": "Saída sem ocorrências"
  }'
```

### 6️⃣ Registrar entrada de veículo

```bash
curl -X POST "http://localhost:8000/acessos-veiculares/" \
  -H "Content-Type: application/json" \
  -d '{
    "id_veiculo": 1,
    "id_responsavel": 1,
    "id_tipo_servico": 1,
    "nota_fiscal_entrada": "NF-123456"
  }'
```

### 7️⃣ Registrar saída de veículo

```bash
curl -X PUT "http://localhost:8000/acessos-veiculares/1/saida" \
  -H "Content-Type: application/json" \
  -d '{
    "nota_fiscal_saida": "NF-123457",
    "observacao": "Coleta realizada"
  }'
```

## Estrutura de Diretórios

```
.
├── app/                          # Pacote principal da aplicação
│   ├── __init__.py
│   ├── database/                 # Configurações do banco
│   │   ├── __init__.py
│   │   ├── config.py            # Configurações (DATABASE_URL, SECRET_KEY)
│   │   └── connection.py        # SessionLocal, engine, get_db()
│   ├── models/                   # Modelos ORM
│   │   ├── __init__.py
│   │   ├── base.py              # Base compartilhada
│   │   ├── usuario.py
│   │   ├── veiculo.py
│   │   ├── acesso_pessoal.py
│   │   └── acesso_veicular.py
│   ├── schemas/                  # Schemas Pydantic
│   │   ├── __init__.py
│   │   ├── usuario_schema.py
│   │   ├── veiculo_schema.py
│   │   ├── acesso_pessoal_schema.py
│   │   └── acesso_veicular_schema.py
│   ├── services/                 # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── usuario_service.py
│   │   ├── veiculo_service.py
│   │   ├── acesso_pessoal_service.py
│   │   └── acesso_veicular_service.py
│   ├── routes/                   # Endpoints da API
│   │   ├── __init__.py
│   │   ├── usuario_routes.py
│   │   ├── veiculo_routes.py
│   │   ├── acesso_pessoal_routes.py
│   │   └── acesso_veicular_routes.py
│   ├── utils/                    # Funções utilitárias
│   │   ├── __init__.py
│   │   └── security.py          # Funções de criptografia e JWT
│   └── main.py                  # FastAPI app (alternativo)
├── main.py                       # Entrada principal
├── run.py                        # Script de inicialização
├── requirements.txt              # Dependências do projeto
├── .env.example                  # Exemplo de variáveis de ambiente
├── README.md                     # Documentação principal
├── GUIDE.md                      # Este arquivo
├── querys/                       # Scripts SQL
│   ├── Query 1.sql              # Criação de tabelas
│   ├── Query 2.sql              # Views
│   ├── Query 3.sql              # Scripts adicionais
└── Listas_aula/                 # Trabalhos anteriores
```

## Solução de Problemas

### Erro: `ModuleNotFoundError: No module named 'app'`

**Solução**: Certifique-se de executar o comando da raiz do projeto (onde `main.py` está localizado).

```bash
cd "c:\Users\adsow\Desktop\trabalho de bd terceiro"
python run.py
```

### Erro: `No module named 'pymysql'`

**Solução**: Instale as dependências:

```bash
pip install -r requirements.txt
```

### Erro de conexão com banco de dados

**Solução**: Verifique:
1. Se MySQL/MariaDB está rodando
2. As credenciais no arquivo `.env`
3. Se o banco `controle_acesso` foi criado

### Porta 8000 em uso

**Solução**: Use outra porta:

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

## Próximos Passos (Melhorias Futuras)

- [ ] Implementar autenticação bearer token nos endpoints protegidos
- [ ] Adicionar testes unitários e de integração
- [ ] Implementar logs detalhados com `logging`
- [ ] Adicionar validação de permissões por role/perfil
- [ ] Criar scripts de seed com dados iniciais
- [ ] Implementar paginação com cursores
- [ ] Adicionar documentação de API com ejemplos reais
- [ ] Implementar rate limiting
- [ ] Adicionar cache com Redis
- [ ] Dockerizar a aplicação

## Dúvidas ou Problemas?

Consulte a documentação no Swagger: http://localhost:8000/docs
