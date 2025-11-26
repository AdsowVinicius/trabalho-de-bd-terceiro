from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Veiculo(Base):
    """Modelo ORM para tabela veiculos"""
    __tablename__ = "veiculos"
    
    id_veiculo = Column(Integer, primary_key=True, index=True)
    placa = Column(String(10), nullable=False, unique=True)
    modelo = Column(String(80), nullable=True)
    ano = Column(Integer, nullable=True)
    id_responsavel = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    responsavel = relationship("Usuario", back_populates="veiculos")
    acessos = relationship("AcessoVeicular", back_populates="veiculo")
    
    def __repr__(self):
        return f"<Veiculo(id={self.id_veiculo}, placa={self.placa}, modelo={self.modelo})>"
