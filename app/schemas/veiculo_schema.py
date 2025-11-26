from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class VeiculoBase(BaseModel):
    """Schema base para Veiculo"""
    placa: str = Field(..., min_length=1, max_length=10)
    modelo: Optional[str] = Field(None, max_length=80)
    ano: Optional[int] = None
    id_responsavel: int


class VeiculoCreate(VeiculoBase):
    """Schema para criação de Veiculo"""
    pass


class VeiculoUpdate(BaseModel):
    """Schema para atualização de Veiculo"""
    modelo: Optional[str] = Field(None, max_length=80)
    ano: Optional[int] = None
    id_responsavel: Optional[int] = None


class VeiculoResponse(VeiculoBase):
    """Schema para resposta de Veiculo"""
    id_veiculo: int
    data_cadastro: datetime
    
    class Config:
        from_attributes = True
