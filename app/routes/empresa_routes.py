from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.services.empresa_service import EmpresaService
from app.schemas.empresa_schema import EmpresaCreate, EmpresaUpdate, EmpresaResponse
from typing import List

router = APIRouter(prefix='/empresas', tags=['empresas'])


@router.post('/', response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
async def criar_empresa(
    empresa_data: EmpresaCreate,
    db: Session = Depends(get_db)
):
    """Cria uma nova empresa"""
    try:
        service = EmpresaService(db)
        empresa = service.criar_empresa(empresa_data)
        return empresa
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao criar empresa: {str(e)}")


@router.get('/', response_model=List[EmpresaResponse])
async def listar_empresas(
    db: Session = Depends(get_db)
):
    """Lista todas as empresas"""
    try:
        service = EmpresaService(db)
        empresas = service.listar_empresas()
        return empresas
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao listar empresas: {str(e)}")


@router.get('/{id_empresa}', response_model=EmpresaResponse)
async def obter_empresa(
    id_empresa: int,
    db: Session = Depends(get_db)
):
    """Obtém uma empresa pelo ID"""
    try:
        service = EmpresaService(db)
        empresa = service.obter_empresa_por_id(id_empresa)
        if not empresa:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
        return empresa
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/cnpj/{cnpj}', response_model=EmpresaResponse)
async def obter_empresa_por_cnpj(
    cnpj: str,
    db: Session = Depends(get_db)
):
    """Obtém uma empresa pelo CNPJ"""
    try:
        service = EmpresaService(db)
        empresa = service.obter_empresa_por_cnpj(cnpj)
        if not empresa:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
        return empresa
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put('/{id_empresa}', response_model=EmpresaResponse)
async def atualizar_empresa(
    id_empresa: int,
    empresa_data: EmpresaUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza uma empresa"""
    try:
        service = EmpresaService(db)
        empresa = service.atualizar_empresa(id_empresa, empresa_data)
        if not empresa:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
        return empresa
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete('/{id_empresa}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_empresa(
    id_empresa: int,
    db: Session = Depends(get_db)
):
    """Deleta uma empresa"""
    try:
        service = EmpresaService(db)
        sucesso = service.deletar_empresa(id_empresa)
        if not sucesso:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


