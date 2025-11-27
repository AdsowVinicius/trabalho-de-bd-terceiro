from sqlalchemy import Column, Integer, String
from .base import Base


class Empresa(Base):
    """Modelo mínimo para a tabela `empresas` necessária por foreign keys"""
    __tablename__ = "empresas"

    id_empresa = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover - convenience
        return f"<Empresa(id_empresa={self.id_empresa}, nome={self.nome})>"
