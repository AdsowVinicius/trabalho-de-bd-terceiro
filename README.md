# Controle de Acesso - API FastAPI + React

Uma aplicacao completa para controle de entrada de pessoas e veiculos, com autenticacao JWT e interface React moderna.

## Características

- ✅ Autenticacao com JWT
- ✅ Criptografia de senhas com pbkdf2_sha256
- ✅ CRUDs completos para usuarios, veiculos, acessos pessoais e veiculares
- ✅ Formularios avancados com autocomplete e busca
- ✅ Auto-preenchimento de campos relacionados
- ✅ Arquitetura em camadas (Models, Services, Routes, Schemas)
- ✅ Integracao com MariaDB/MySQL
- ✅ Frontend React com Vite
- ✅ Documentacao automatica com Swagger
- ✅ Boas praticas de OOP e encapsulamento

## 🚀 Quick Start

### Backend
```bash
cd "c:\Users\adsow\Desktop\trabalho de bd terceiro"
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Acessar
- **Aplicacao**: http://localhost:5174
- **API Docs**: http://127.0.0.1:8001/docs

## Estrutura do Projeto

```
app/
├── database/          # Configuração do banco de dados
│   ├── __init__.py
│   ├── config.py      # Configurações da aplicação
│   └── connection.py  # Conexão com banco de dados
├── models/            # Modelos ORM (SQLAlchemy)
│   ├── __init__.py
│   ├── usuario.py
│   ├── veiculo.py
│   ├── acesso_pessoal.py
│   └── acesso_veicular.py
├── schemas/           # Schemas Pydantic para validação
│   ├── __init__.py
│   ├── usuario_schema.py
│   ├── veiculo_schema.py
│   ├── acesso_pessoal_schema.py
│   └── acesso_veicular_schema.py
├── services/          # Lógica de negócio
│   ├── __init__.py
│   ├── usuario_service.py
│   ├── veiculo_service.py
│   ├── acesso_pessoal_service.py
│   └── acesso_veicular_service.py
├── routes/            # Endpoints da API
│   ├── __init__.py
│   ├── usuario_routes.py
│   ├── veiculo_routes.py
│   ├── acesso_pessoal_routes.py
│   └── acesso_veicular_routes.py
├── utils/             # Funções utilitárias
│   ├── __init__.py
│   └── security.py    # Funções de segurança
└── __init__.py

main.py               # Arquivo principal da aplicação
requirements.txt      # Dependências do projeto
.env.example         # Exemplo de variáveis de ambiente
```

## Instalação

### Pré-requisitos
- Python 3.10+
- MariaDB ou MySQL
- pip

### Passos

1. **Clone ou baixe o projeto**

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure o banco de dados**
   - Execute os scripts SQL (`Query 1.sql` e `Query 2.sql`)
   - Configure as credenciais de banco em `.env`

4. **Crie um arquivo `.env`**
```bash
copy .env.example .env
```

5. **Inicie a aplicação**
```bash
python main.py
```

A API estará disponível em: `http://localhost:8000`

## Endpoints

### Autenticação (Usuários)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/usuarios/registro` | Registrar novo usuário |
| POST | `/usuarios/login` | Login e obter token JWT |
| GET | `/usuarios/{usuario_id}` | Obter dados de um usuário |
| GET | `/usuarios/` | Listar todos os usuários |
| PUT | `/usuarios/{usuario_id}` | Atualizar usuário |
| DELETE | `/usuarios/{usuario_id}` | Deletar usuário |

### Veículos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/veiculos/` | Registrar novo veículo |
| GET | `/veiculos/{veiculo_id}` | Obter dados de um veículo |
| GET | `/veiculos/placa/{placa}` | Obter veículo pela placa |
| GET | `/veiculos/responsavel/{responsavel_id}` | Listar veículos de um responsável |
| GET | `/veiculos/` | Listar todos os veículos |
| PUT | `/veiculos/{veiculo_id}` | Atualizar veículo |
| DELETE | `/veiculos/{veiculo_id}` | Deletar veículo |

### Acessos Pessoais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/acessos-pessoais/` | Registrar entrada de pessoa |
| GET | `/acessos-pessoais/{acesso_id}` | Obter dados de um acesso |
| GET | `/acessos-pessoais/usuario/{usuario_id}` | Listar acessos de um usuário |
| GET | `/acessos-pessoais/` | Listar todos os acessos |
| GET | `/acessos-pessoais/ativos/visitantes` | Listar visitantes atualmente dentro |
| PUT | `/acessos-pessoais/{acesso_id}/saida` | Registrar saída de pessoa |
| PUT | `/acessos-pessoais/{acesso_id}` | Atualizar acesso |
| DELETE | `/acessos-pessoais/{acesso_id}` | Deletar acesso |

### Acessos Veiculares

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/acessos-veiculares/` | Registrar entrada de veículo |
| GET | `/acessos-veiculares/{acesso_id}` | Obter dados de um acesso |
| GET | `/acessos-veiculares/veiculo/{veiculo_id}` | Listar acessos de um veículo |
| GET | `/acessos-veiculares/responsavel/{responsavel_id}` | Listar acessos de um responsável |
| GET | `/acessos-veiculares/` | Listar todos os acessos |
| GET | `/acessos-veiculares/ativos/veiculos` | Listar veículos atualmente dentro |
| PUT | `/acessos-veiculares/{acesso_id}/saida` | Registrar saída de veículo |
| PUT | `/acessos-veiculares/{acesso_id}` | Atualizar acesso |
| DELETE | `/acessos-veiculares/{acesso_id}` | Deletar acesso |

## Exemplo de Uso

### 1. Registrar um novo usuário

```bash
curl -X POST "http://localhost:8000/usuarios/registro" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "documento": "12345678900",
    "id_tipo_usuario": 1,
    "login": "joao",
    "senha": "123456",
    "id_perfil_acesso": 1,
    "contato": "11999999999"
  }'
```

### 2. Fazer login

```bash
curl -X POST "http://localhost:8000/usuarios/login" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "joao",
    "senha": "123456"
  }'
```

### 3. Registrar um veículo

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

### 4. Registrar entrada de pessoa

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

### 5. Registrar saída de pessoa

```bash
curl -X PUT "http://localhost:8000/acessos-pessoais/1/saida" \
  -H "Content-Type: application/json" \
  -d '{
    "observacao": "Saída normal"
  }'
```

## Boas Práticas Implementadas

1. **Separação de Responsabilidades**
   - Models: Definem a estrutura dos dados
   - Services: Implementam a lógica de negócio
   - Routes: Expõem os endpoints
   - Schemas: Validam os dados de entrada

2. **Encapsulamento**
   - Cada Service encapsula a lógica relacionada a uma entidade
   - Database abstração através de dependência injetada

3. **Segurança**
   - Senhas criptografadas com bcrypt
   - Tokens JWT para autenticação
   - Validação de entrada com Pydantic

4. **Tratamento de Erros**
   - HTTPExceptions apropriadas
   - Mensagens de erro informativas

5. **Documentação**
   - Docstrings em todas as funções
   - Swagger automático em `/docs`
   - Comentários explicativos no código

## Próximos Passos

- [ ] Implementar autenticação por token nas rotas
- [ ] Adicionar testes unitários
- [ ] Implementar logs
- [ ] Adicionar validação de permissões por role
- [ ] Criar scripts de seed para dados iniciais
- [ ] Implementar paginação avançada com cursores

## Licença

MIT

## Contato

Para dúvidas ou sugestões, abra uma issue no repositório.
