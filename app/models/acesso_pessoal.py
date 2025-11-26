from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class AcessoPessoal(Base):
    """Modelo ORM para tabela acessos_pessoais"""
    __tablename__ = "acessos_pessoais"
    
    id_acesso_pessoal = Column(Integer, primary_key=True, index=True)
    data_registro = Column(DateTime, default=datetime.utcnow, nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    documento_usuario = Column(String(30), nullable=True)
    id_tipo_acesso = Column(Integer, ForeignKey("lu_tipos_servico.id"), nullable=False)
    id_empresa_visitada = Column(Integer, ForeignKey("empresas.id_empresa"), nullable=True)
    motivo_visita = Column(String(255), nullable=True)
    hora_entrada = Column(DateTime, default=datetime.utcnow, nullable=False)
    hora_saida = Column(DateTime, nullable=True)
    observacao = Column(Text, nullable=True)
    
    # Relacionamentos
    usuario = relationship("Usuario", back_populates="acessos_pessoais")
    
    def __repr__(self):
        return f"<AcessoPessoal(id={self.id_acesso_pessoal}, usuario={self.id_usuario})>"
