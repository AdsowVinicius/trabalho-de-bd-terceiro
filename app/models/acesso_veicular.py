from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class AcessoVeicular(Base):
    """Modelo ORM para tabela acessos_veiculares"""
    __tablename__ = "acessos_veiculares"
    
    id_acesso_veiculo = Column(Integer, primary_key=True, index=True)
    data_registro = Column(DateTime, default=datetime.utcnow, nullable=False)
    id_veiculo = Column(Integer, ForeignKey("veiculos.id_veiculo"), nullable=False)
    placa = Column(String(10), nullable=True)
    id_responsavel = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    ano_veiculo = Column(Integer, nullable=True)
    hora_entrada = Column(DateTime, default=datetime.utcnow, nullable=False)
    hora_saida = Column(DateTime, nullable=True)
    id_tipo_servico = Column(Integer, ForeignKey("lu_tipos_servico.id"), nullable=False)
    nota_fiscal_entrada = Column(String(80), nullable=True)
    nota_fiscal_saida = Column(String(80), nullable=True)
    id_transportadora = Column(Integer, ForeignKey("empresas.id_empresa"), nullable=True)
    observacao = Column(Text, nullable=True)
    
    # Relacionamentos
    veiculo = relationship("Veiculo", back_populates="acessos")
    responsavel = relationship("Usuario", back_populates="acessos_veiculares")
    
    def __repr__(self):
        return f"<AcessoVeicular(id={self.id_acesso_veiculo}, veiculo={self.id_veiculo})>"
