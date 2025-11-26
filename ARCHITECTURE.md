# 🏗️ Arquitetura do Projeto

## Diagrama de Fluxo

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT/FRONTEND                        │
├─────────────────────────────────────────────────────────────┤
│ (Navegador, Mobile App, Cliente HTTP, etc)                  │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI FRAMEWORK                        │
├─────────────────────────────────────────────────────────────┤
│  ▪ CORS Middleware                                          │
│  ▪ Request/Response Validation                              │
│  ▪ OpenAPI Documentation (Swagger)                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      ROUTES LAYER                           │
├─────────────────────────────────────────────────────────────┤
│  ├── usuario_routes.py                                      │
│  │   ├── POST   /usuarios/registro      (Registrar)        │
│  │   ├── POST   /usuarios/login         (Autenticar)       │
│  │   ├── GET    /usuarios/{id}          (Obter)            │
│  │   ├── GET    /usuarios/              (Listar)           │
│  │   ├── PUT    /usuarios/{id}          (Atualizar)        │
│  │   └── DELETE /usuarios/{id}          (Deletar)          │
│  │                                                          │
│  ├── veiculo_routes.py                                      │
│  │   ├── POST   /veiculos/              (Criar)            │
│  │   ├── GET    /veiculos/{id}          (Obter)            │
│  │   ├── GET    /veiculos/              (Listar)           │
│  │   ├── PUT    /veiculos/{id}          (Atualizar)        │
│  │   └── DELETE /veiculos/{id}          (Deletar)          │
│  │                                                          │
│  ├── acesso_pessoal_routes.py                               │
│  │   ├── POST   /acessos-pessoais/      (Registrar entrada)│
│  │   ├── GET    /acessos-pessoais/{id}  (Obter)            │
│  │   ├── GET    /acessos-pessoais/      (Listar)           │
│  │   ├── PUT    /acessos-pessoais/{id}/saida (Saída)      │
│  │   └── DELETE /acessos-pessoais/{id}  (Deletar)          │
│  │                                                          │
│  └── acesso_veicular_routes.py                              │
│      ├── POST   /acessos-veiculares/    (Registrar entrada)│
│      ├── GET    /acessos-veiculares/{id}(Obter)            │
│      ├── GET    /acessos-veiculares/    (Listar)           │
│      ├── PUT    /acessos-veiculares/{id}/saida (Saída)    │
│      └── DELETE /acessos-veiculares/{id}(Deletar)          │
│                                                          │
└────────────────────────┬────────────────────────────────────┘
                         │ Dependências Injetadas
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    SERVICES LAYER                           │
├─────────────────────────────────────────────────────────────┤
│  ├── UsuarioService                                         │
│  │   ├── criar_usuario()                                   │
│  │   ├── obter_usuario_por_id()                            │
│  │   ├── obter_usuario_por_login()                         │
│  │   ├── listar_usuarios()                                 │
│  │   ├── atualizar_usuario()                               │
│  │   ├── deletar_usuario()                                 │
│  │   └── autenticar_usuario()                              │
│  │                                                          │
│  ├── VeiculoService                                         │
│  │   ├── criar_veiculo()                                   │
│  │   ├── obter_veiculo_por_id()                            │
│  │   ├── obter_veiculo_por_placa()                         │
│  │   ├── listar_veiculos()                                 │
│  │   ├── atualizar_veiculo()                               │
│  │   └── deletar_veiculo()                                 │
│  │                                                          │
│  ├── AcessoPessoalService                                   │
│  │   ├── criar_acesso()                                    │
│  │   ├── obter_acesso_por_id()                             │
│  │   ├── listar_acessos()                                  │
│  │   ├── listar_visitantes_ativos()                        │
│  │   ├── registrar_saida()                                 │
│  │   └── deletar_acesso()                                  │
│  │                                                          │
│  └── AcessoVeicularService                                  │
│      ├── criar_acesso()                                    │
│      ├── obter_acesso_por_id()                             │
│      ├── listar_acessos()                                  │
│      ├── listar_veiculos_ativos()                          │
│      ├── registrar_saida()                                 │
│      └── deletar_acesso()                                  │
│                                                          │
└────────────────────────┬────────────────────────────────────┘
                         │ SQLAlchemy ORM
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    MODELS LAYER (ORM)                       │
├─────────────────────────────────────────────────────────────┤
│  ├── Usuario                                                │
│  │   ├── id_usuario (PK)                                   │
│  │   ├── nome                                              │
│  │   ├── documento (UNIQUE)                                │
│  │   ├── id_tipo_usuario (FK)                              │
│  │   ├── login (UNIQUE)                                    │
│  │   ├── senha_hash                                        │
│  │   ├── id_perfil_acesso (FK)                             │
│  │   ├── empresa_origem (FK)                               │
│  │   ├── ativo                                             │
│  │   └── data_cadastro                                     │
│  │                                                          │
│  ├── Veiculo                                                │
│  │   ├── id_veiculo (PK)                                   │
│  │   ├── placa (UNIQUE)                                    │
│  │   ├── modelo                                            │
│  │   ├── ano                                               │
│  │   ├── id_responsavel (FK → Usuario)                     │
│  │   └── data_cadastro                                     │
│  │                                                          │
│  ├── AcessoPessoal                                          │
│  │   ├── id_acesso_pessoal (PK)                            │
│  │   ├── data_registro                                     │
│  │   ├── id_usuario (FK → Usuario)                         │
│  │   ├── id_tipo_acesso (FK)                               │
│  │   ├── id_empresa_visitada (FK)                          │
│  │   ├── motivo_visita                                     │
│  │   ├── hora_entrada                                      │
│  │   ├── hora_saida                                        │
│  │   └── observacao                                        │
│  │                                                          │
│  └── AcessoVeicular                                         │
│      ├── id_acesso_veiculo (PK)                            │
│      ├── data_registro                                     │
│      ├── id_veiculo (FK → Veiculo)                         │
│      ├── id_responsavel (FK → Usuario)                     │
│      ├── id_tipo_servico (FK)                              │
│      ├── id_transportadora (FK)                            │
│      ├── nota_fiscal_entrada                               │
│      ├── nota_fiscal_saida                                 │
│      ├── hora_entrada                                      │
│      ├── hora_saida                                        │
│      └── observacao                                        │
│                                                          │
└────────────────────────┬────────────────────────────────────┘
                         │ SQL
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  DATABASE LAYER                             │
├─────────────────────────────────────────────────────────────┤
│  ├── MySQL/MariaDB Connection                              │
│  │   └── controle_acesso (Database)                        │
│  │       ├── usuarios                                      │
│  │       ├── veiculos                                      │
│  │       ├── acessos_pessoais                              │
│  │       ├── acessos_veiculares                            │
│  │       ├── lu_tipos_empresa                              │
│  │       ├── lu_tipos_usuario                              │
│  │       ├── lu_perfis_acesso                              │
│  │       ├── lu_tipos_servico                              │
│  │       ├── empresas                                      │
│  │       ├── audit_log                                     │
│  │       ├── vw_acessos_pessoais_detalhado                │
│  │       ├── vw_acessos_veiculares_detalhado              │
│  │       ├── vw_visitantes_ativos                          │
│  │       └── vw_veiculos_ativos                            │
│                                                          │
└─────────────────────────────────────────────────────────────┘
```

## Fluxo de Requisição Típico

```
1. Cliente faz requisição HTTP
   ├── POST /usuarios/login
   └── Payload: {"login": "joao", "senha": "123456"}

2. FastAPI route intercepta a requisição
   ├── Valida schema Pydantic (UsuarioLogin)
   ├── Injeta dependência (Session do DB)
   └── Chama função do route

3. Route cria instância do service
   ├── UsuarioService(db)
   └── Chama service.autenticar_usuario()

4. Service executa lógica de negócio
   ├── Consulta usuário no banco
   ├── Verifica senha com bcrypt
   ├── Verifica se está ativo
   └── Cria token JWT

5. Route retorna resposta
   ├── Serializa modelo com Pydantic
   ├── Retorna JSON com status 200
   └── Cliente recebe resposta

6. Erro (se ocorrer)
   ├── Service levanta ValueError
   ├── Route captura exceção
   ├── Retorna HTTPException apropriada
   └── Cliente recebe erro com status correto
```

## Padrões de Design Utilizados

### 1. **Service Pattern**
Cada entidade tem um Service que encapsula toda lógica de negócio
```python
class UsuarioService:
    def __init__(self, db: Session):
        self.db = db
    
    def criar_usuario(self, dados: UsuarioCreate) -> Usuario:
        # Lógica aqui
        pass
```

### 2. **Dependency Injection**
Dependências injetadas via FastAPI Depends()
```python
@app.get("/usuarios/{id}")
def obter(usuario_id: int, db: Session = Depends(get_db)):
    service = UsuarioService(db)
    # Usar service
```

### 3. **Schema Validation (Pydantic)**
Validação de entrada e saída com Pydantic
```python
class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=1)
    login: str = Field(..., min_length=1)
    senha: str = Field(..., min_length=6)
```

### 4. **Repository Pattern (implícito)**
Database abstração via SQLAlchemy ORM
```python
usuario = self.db.query(Usuario).filter(...).first()
```

## Segurança

### Criptografia
- **Senhas**: bcrypt (passlib)
- **Tokens**: JWT (python-jose)

### Validação
- **Input**: Pydantic schemas
- **Output**: ORM models serializados

### CORS
- Configurado para aceitar requisições de qualquer origem
- Em produção, especificar domínios permitidos

## Performance

### Índices no Banco
```sql
CREATE INDEX idx_usuarios_documento ON usuarios(documento);
CREATE INDEX idx_acessos_pessoais_usuario ON acessos_pessoais(id_usuario);
CREATE INDEX idx_acessos_veic_placa ON acessos_veiculares(placa);
CREATE INDEX idx_acessos_veic_veiculo ON acessos_veiculares(id_veiculo);
```

### Connection Pooling
```python
engine = create_engine(
    url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

## Próximas Otimizações

- [ ] Implementar cache com Redis
- [ ] Adicionar rate limiting
- [ ] Paginação com cursores
- [ ] Query optimization
- [ ] Database sharding (se necessário)
