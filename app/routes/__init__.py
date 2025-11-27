from .usuario_routes import router as usuario_router
from .veiculo_routes import router as veiculo_router
from .acesso_pessoal_routes import router as acesso_pessoal_router
from .acesso_veicular_routes import router as acesso_veicular_router
from .lookups_routes import router as lookups_router

__all__ = [
    "usuario_router",
    "veiculo_router",
    "acesso_pessoal_router",
    "acesso_veicular_router",
    "lookups_router",
]
