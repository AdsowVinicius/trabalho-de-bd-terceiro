from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import VeiculoCreate, VeiculoUpdate, VeiculoResponse
from ..services.veiculo_service import VeiculoService

router = APIRouter(prefix="/veiculos", tags=["Veículos"])


@router.post("/", response_model=VeiculoResponse, status_code=status.HTTP_201_CREATED)
async def criar_veiculo(
    veiculo_data: VeiculoCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo veículo
    
    - **placa**: Placa do veículo (única)
    - **modelo**: Modelo do veículo
    - **ano**: Ano de fabricação
    - **id_responsavel**: ID do usuário responsável
    """
    try:
        service = VeiculoService(db)
        veiculo = service.criar_veiculo(veiculo_data)
        return veiculo
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{veiculo_id}", response_model=VeiculoResponse)
async def obter_veiculo(
    veiculo_id: int,
    db: Session = Depends(get_db)
):
    """Obtém informações de um veículo específico"""
    service = VeiculoService(db)
    veiculo = service.obter_veiculo_por_id(veiculo_id)
    
    if not veiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado"
        )
    
    return veiculo


@router.get("/placa/{placa}", response_model=VeiculoResponse)
async def obter_veiculo_por_placa(
    placa: str,
    db: Session = Depends(get_db)
):
    """Obtém informações de um veículo pela placa"""
    service = VeiculoService(db)
    veiculo = service.obter_veiculo_por_placa(placa)
    
    if not veiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado"
        )
    
    return veiculo


@router.get("/responsavel/{responsavel_id}", response_model=list[VeiculoResponse])
async def listar_veiculos_por_responsavel(
    responsavel_id: int,
    db: Session = Depends(get_db)
):
    """Lista veículos de um responsável"""
    service = VeiculoService(db)
    veiculos = service.listar_veiculos_por_responsavel(responsavel_id)
    return veiculos


@router.get("/", response_model=list[VeiculoResponse])
async def listar_veiculos(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Lista todos os veículos com paginação"""
    service = VeiculoService(db)
    veiculos = service.listar_veiculos(skip=skip, limit=limit)
    return veiculos


@router.put("/{veiculo_id}", response_model=VeiculoResponse)
async def atualizar_veiculo(
    veiculo_id: int,
    veiculo_data: VeiculoUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um veículo existente"""
    try:
        service = VeiculoService(db)
        veiculo = service.atualizar_veiculo(veiculo_id, veiculo_data)
        
        if not veiculo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Veículo não encontrado"
            )
        
        return veiculo
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{veiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_veiculo(
    veiculo_id: int,
    db: Session = Depends(get_db)
):
    """Deleta um veículo"""
    try:
        service = VeiculoService(db)
        sucesso = service.deletar_veiculo(veiculo_id)
        
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Veículo não encontrado"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
