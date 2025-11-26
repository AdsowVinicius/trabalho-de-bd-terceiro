from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import AcessoPessoalCreate, AcessoPessoalUpdate, AcessoPessoalResponse, AcessoPessoalDetalhado
from ..services.acesso_pessoal_service import AcessoPessoalService

router = APIRouter(prefix="/acessos-pessoais", tags=["Acessos Pessoais"])


@router.post("/", response_model=AcessoPessoalResponse, status_code=status.HTTP_201_CREATED)
async def registrar_entrada_pessoal(
    acesso_data: AcessoPessoalCreate,
    db: Session = Depends(get_db)
):
    """
    Registra a entrada de uma pessoa
    
    - **id_usuario**: ID do usuário que está entrando
    - **id_tipo_acesso**: Tipo de acesso
    - **id_empresa_visitada**: ID da empresa visitada (opcional)
    - **motivo_visita**: Motivo da visita (opcional)
    - **observacao**: Observações (opcional)
    """
    try:
        service = AcessoPessoalService(db)
        acesso = service.criar_acesso(acesso_data)
        return acesso
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{acesso_id}", response_model=AcessoPessoalResponse)
async def obter_acesso(
    acesso_id: int,
    db: Session = Depends(get_db)
):
    """Obtém informações de um acesso específico"""
    service = AcessoPessoalService(db)
    acesso = service.obter_acesso_por_id(acesso_id)
    
    if not acesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Acesso não encontrado"
        )
    
    return acesso


@router.get("/usuario/{usuario_id}", response_model=list[AcessoPessoalResponse])
async def listar_acessos_por_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """Lista todos os acessos de um usuário específico"""
    service = AcessoPessoalService(db)
    acessos = service.listar_acessos_por_usuario(usuario_id)
    return acessos


@router.get("/", response_model=list[AcessoPessoalResponse])
async def listar_acessos(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Lista todos os acessos com paginação"""
    service = AcessoPessoalService(db)
    acessos = service.listar_acessos(skip=skip, limit=limit)
    return acessos


@router.get("/ativos/visitantes", response_model=list[AcessoPessoalResponse])
async def listar_visitantes_ativos(db: Session = Depends(get_db)):
    """Lista visitantes atualmente dentro (sem hora de saída)"""
    service = AcessoPessoalService(db)
    acessos = service.listar_visitantes_ativos()
    return acessos


@router.put("/{acesso_id}/saida", response_model=AcessoPessoalResponse)
async def registrar_saida(
    acesso_id: int,
    acesso_data: AcessoPessoalUpdate,
    db: Session = Depends(get_db)
):
    """Registra a saída de uma pessoa"""
    try:
        service = AcessoPessoalService(db)
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


@router.put("/{acesso_id}", response_model=AcessoPessoalResponse)
async def atualizar_acesso(
    acesso_id: int,
    acesso_data: AcessoPessoalUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um acesso existente"""
    try:
        service = AcessoPessoalService(db)
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
        service = AcessoPessoalService(db)
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
