from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import (
    usuario_router,
    veiculo_router,
    acesso_pessoal_router,
    acesso_veicular_router,
    lookups_router,
    empresa_router,
    relatorios_router,
)
from app.database import engine
from app.models import Base


# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Configuração do ciclo de vida da aplicação"""
    # Startup
    print("Iniciando aplicação...")
    # Debug: listar rotas registradas para diagnóstico
    try:
        print("Rotas registradas:")
        for r in app.router.routes:
            path = getattr(r, "path", None) or getattr(r, "pattern", None) or str(r)
            methods = getattr(r, "methods", None) or set()
            print(f"  {path} {methods}")
    except Exception as _err:
        print("Erro ao listar rotas:", _err)
    # Criar tabelas se não existirem
    # Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    print("Encerrando aplicação...")


# Criar aplicação FastAPI
app = FastAPI(
    title="Controle de Acesso - API",
    description="API para controle de entrada de pessoas e veículos",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    # Allow common local frontend dev origins (Vite, static server).
    # Must be explicit when `allow_credentials=True`.
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(usuario_router)
app.include_router(veiculo_router)
app.include_router(acesso_pessoal_router)
app.include_router(acesso_veicular_router)
app.include_router(lookups_router)
app.include_router(empresa_router)
app.include_router(relatorios_router)


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raiz da API"""
    return {
        "mensagem": "Bem-vindo à API de Controle de Acesso",
        "versao": "1.0.0",
        "documentacao": "/docs"
    }



@app.get("/health", tags=["Health"])
async def health_check():
    """Verifica o status da aplicação"""
    return {
        "status": "ok",
        "servico": "Controle de Acesso"
    }

