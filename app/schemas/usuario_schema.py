from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UsuarioBase(BaseModel):
    """Schema base para Usuario"""
    nome: str = Field(..., min_length=1, max_length=120)
    documento: str = Field(..., min_length=1, max_length=30)
    id_tipo_usuario: int
    id_perfil_acesso: int
    empresa_origem: Optional[int] = None
    contato: Optional[str] = Field(None, max_length=60)
    ativo: bool = True


class UsuarioCreate(UsuarioBase):
    """Schema para criação de Usuario"""
    login: str = Field(..., min_length=1, max_length=80)
    senha: str = Field(..., min_length=6)


class UsuarioUpdate(BaseModel):
    """Schema para atualização de Usuario"""
    nome: Optional[str] = Field(None, min_length=1, max_length=120)
    contato: Optional[str] = Field(None, max_length=60)
    ativo: Optional[bool] = None
    empresa_origem: Optional[int] = None


class UsuarioResponse(UsuarioBase):
    """Schema para resposta de Usuario"""
    id_usuario: int
    login: Optional[str] = None
    data_cadastro: datetime
    
    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    """Schema para login"""
    login: str = Field(..., min_length=1)
    senha: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """Schema para resposta de token"""
    access_token: str
    token_type: str
    usuario: UsuarioResponse
