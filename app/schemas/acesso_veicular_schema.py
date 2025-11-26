from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AcessoVeicularBase(BaseModel):
    """Schema base para AcessoVeicular"""
    id_veiculo: int
    id_responsavel: int
    id_tipo_servico: int
    id_transportadora: Optional[int] = None
    nota_fiscal_entrada: Optional[str] = Field(None, max_length=80)
    nota_fiscal_saida: Optional[str] = Field(None, max_length=80)
    observacao: Optional[str] = None


class AcessoVeicularCreate(AcessoVeicularBase):
    """Schema para criação de AcessoVeicular"""
    pass


class AcessoVeicularUpdate(BaseModel):
    """Schema para atualização de AcessoVeicular"""
    hora_saida: Optional[datetime] = None
    nota_fiscal_saida: Optional[str] = Field(None, max_length=80)
    observacao: Optional[str] = None


class AcessoVeicularResponse(AcessoVeicularBase):
    """Schema para resposta de AcessoVeicular"""
    id_acesso_veiculo: int
    data_registro: datetime
    placa: Optional[str] = None
    ano_veiculo: Optional[int] = None
    hora_entrada: datetime
    hora_saida: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AcessoVeicularDetalhado(BaseModel):
    """Schema detalhado de AcessoVeicular com informações relacionadas"""
    id_acesso_veiculo: int
    data_registro: datetime
    placa: str
    modelo: Optional[str] = None
    nome_responsavel: str
    transportadora: Optional[str] = None
    tipo_servico: Optional[str] = None
    nota_fiscal_entrada: Optional[str] = None
    nota_fiscal_saida: Optional[str] = None
    hora_entrada: datetime
    hora_saida: Optional[datetime] = None
    observacao: Optional[str] = None
