from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import AcessoVeicularCreate, AcessoVeicularUpdate, AcessoVeicularResponse, AcessoVeicularDetalhado
from ..services.acesso_veicular_service import AcessoVeicularService

router = APIRouter(prefix="/acessos-veiculares", tags=["Acessos Veiculares"])


@router.post("/", response_model=AcessoVeicularResponse, status_code=status.HTTP_201_CREATED)
async def registrar_entrada_veicular(
    acesso_data: AcessoVeicularCreate,
    db: Session = Depends(get_db)
):
    """
    Registra a entrada de um veículo
    
    - **id_veiculo**: ID do veículo
    - **id_responsavel**: ID do usuário responsável
    - **id_tipo_servico**: Tipo de serviço
    - **id_transportadora**: ID da transportadora (opcional)
    - **nota_fiscal_entrada**: Nota fiscal de entrada (opcional)
    - **observacao**: Observações (opcional)
    """
    try:
        service = AcessoVeicularService(db)
        acesso = service.criar_acesso(acesso_data)
        return acesso
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{acesso_id}", response_model=AcessoVeicularResponse)
async def obter_acesso(
    acesso_id: int,
    db: Session = Depends(get_db)
):
    """Obtém informações de um acesso específico"""
    service = AcessoVeicularService(db)
    acesso = service.obter_acesso_por_id(acesso_id)
    
    if not acesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Acesso não encontrado"
        )
    
    return acesso


@router.get("/veiculo/{veiculo_id}", response_model=list[AcessoVeicularResponse])
async def listar_acessos_por_veiculo(
    veiculo_id: int,
    db: Session = Depends(get_db)
):
    """Lista todos os acessos de um veículo específico"""
    service = AcessoVeicularService(db)
    acessos = service.listar_acessos_por_veiculo(veiculo_id)
    return acessos


@router.get("/responsavel/{responsavel_id}", response_model=list[AcessoVeicularResponse])
async def listar_acessos_por_responsavel(
    responsavel_id: int,
    db: Session = Depends(get_db)
):
    """Lista todos os acessos de um responsável específico"""
    service = AcessoVeicularService(db)
    acessos = service.listar_acessos_por_responsavel(responsavel_id)
    return acessos


@router.get("/", response_model=list[AcessoVeicularResponse])
async def listar_acessos(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Lista todos os acessos com paginação"""
    service = AcessoVeicularService(db)
    acessos = service.listar_acessos(skip=skip, limit=limit)
    return acessos


@router.get("/ativos/veiculos", response_model=list[AcessoVeicularResponse])
async def listar_veiculos_ativos(db: Session = Depends(get_db)):
    """Lista veículos atualmente dentro (sem hora de saída)"""
    service = AcessoVeicularService(db)
    acessos = service.listar_veiculos_ativos()
    return acessos


@router.put("/{acesso_id}/saida", response_model=AcessoVeicularResponse)
async def registrar_saida(
    acesso_id: int,
    acesso_data: AcessoVeicularUpdate,
    db: Session = Depends(get_db)
):
    """Registra a saída de um veículo"""
    try:
        service = AcessoVeicularService(db)
        acesso = service.registrar_saida(acesso_id, acesso_data)
        
        if not acesso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Acesso não encontrado"
            )
        
        return acesso
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{acesso_id}", response_model=AcessoVeicularResponse)
async def atualizar_acesso(
    acesso_id: int,
    acesso_data: AcessoVeicularUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um acesso existente"""
    try:
        service = AcessoVeicularService(db)
        acesso = service.atualizar_acesso(acesso_id, acesso_data)
        
        if not acesso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Acesso não encontrado"
            )
        
        return acesso
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{acesso_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_acesso(
    acesso_id: int,
    db: Session = Depends(get_db)
):
    """Deleta um acesso"""
    try:
        service = AcessoVeicularService(db)
        sucesso = service.deletar_acesso(acesso_id)
        
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Acesso não encontrado"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
