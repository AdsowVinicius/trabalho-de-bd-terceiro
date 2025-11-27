from sqlalchemy import Column, Integer, String
from .base import Base


class LuPerfisAcesso(Base):
    __tablename__ = "lu_perfis_acesso"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False)


class LuTiposUsuario(Base):
    __tablename__ = "lu_tipos_usuario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False)


class LuTiposEmpresa(Base):
    __tablename__ = "lu_tipos_empresa"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False)


class LuTiposServico(Base):
    __tablename__ = "lu_tipos_servico"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False)
