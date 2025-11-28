from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Usuario(Base):
    """Modelo ORM para tabela usuarios"""
    __tablename__ = "usuarios"
    
    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    documento = Column(String(30), nullable=False, unique=True)
    id_tipo_usuario = Column(Integer, ForeignKey("lu_tipos_usuario.id"), nullable=False)
    login = Column(String(80), unique=True, nullable=True)
    senha_hash = Column(String(255), nullable=True)
    id_perfil_acesso = Column(Integer, ForeignKey("lu_perfis_acesso.id"), nullable=True)
    empresa_origem = Column(Integer, ForeignKey("empresas.id_empresa"), nullable=True)
    contato = Column(String(60), nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    acessos_pessoais = relationship("AcessoPessoal", back_populates="usuario")
    veiculos = relationship("Veiculo", back_populates="responsavel")
    acessos_veiculares = relationship("AcessoVeicular", back_populates="responsavel")
    
    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, nome={self.nome}, login={self.login})>"

