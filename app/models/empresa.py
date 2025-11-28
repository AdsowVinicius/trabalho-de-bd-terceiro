from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from .base import Base


class Empresa(Base):
    """Modelo para a tabela `empresas`"""
    __tablename__ = "empresas"

    id_empresa = Column(Integer, primary_key=True, autoincrement=True)
    nome_empresa = Column(String(120), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=True)
    id_tipo_empresa = Column(Integer, nullable=False)
    responsavel = Column(String(100), nullable=True)
    contato = Column(String(50), nullable=True)
    data_cadastro = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:  # pragma: no cover - convenience
        return f"<Empresa(id_empresa={self.id_empresa}, nome_empresa={self.nome_empresa}, cnpj={self.cnpj})>"

