from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AcessoPessoalBase(BaseModel):
    """Schema base para AcessoPessoal"""
    id_usuario: int
    id_tipo_acesso: int
    id_empresa_visitada: Optional[int] = None
    motivo_visita: Optional[str] = Field(None, max_length=255)
    observacao: Optional[str] = None


class AcessoPessoalCreate(AcessoPessoalBase):
    """Schema para criação de AcessoPessoal"""
    pass


class AcessoPessoalUpdate(BaseModel):
    """Schema para atualização de AcessoPessoal"""
    hora_saida: Optional[datetime] = None
    observacao: Optional[str] = None
    motivo_visita: Optional[str] = Field(None, max_length=255)


class AcessoPessoalResponse(AcessoPessoalBase):
    """Schema para resposta de AcessoPessoal"""
    id_acesso_pessoal: int
    data_registro: datetime
    documento_usuario: Optional[str] = None
    hora_entrada: datetime
    hora_saida: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AcessoPessoalDetalhado(BaseModel):
    """Schema detalhado de AcessoPessoal com informações relacionadas"""
    id_acesso_pessoal: int
    data_registro: datetime
    nome_usuario: str
    documento_cadastrado: str
    tipo_acesso: Optional[str] = None
    empresa_visitada: Optional[str] = None
    motivo_visita: Optional[str] = None
    hora_entrada: datetime
    hora_saida: Optional[datetime] = None
    observacao: Optional[str] = None
