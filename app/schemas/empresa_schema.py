from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EmpresaCreate(BaseModel):
    nome_empresa: str
    cnpj: str
    id_tipo_empresa: int
    responsavel: Optional[str] = None
    contato: Optional[str] = None


class EmpresaUpdate(BaseModel):
    nome_empresa: str
    cnpj: str
    id_tipo_empresa: int
    responsavel: Optional[str] = None
    contato: Optional[str] = None


class EmpresaResponse(BaseModel):
    id_empresa: int
    nome_empresa: str
    cnpj: str
    id_tipo_empresa: int
    responsavel: Optional[str] = None
    contato: Optional[str] = None
    data_cadastro: datetime

    class Config:
        from_attributes = True
