from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import get_db
from ..database.config import settings
from ..schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioLogin, TokenResponse
from ..services.usuario_service import UsuarioService
from ..utils.security import SecurityService

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def registrar_usuario(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """
    Registra um novo usuário
    
    - **nome**: Nome completo do usuário
    - **documento**: CPF/CNPJ ou documento único
    - **id_tipo_usuario**: ID do tipo de usuário
    - **login**: Login único para acesso
    - **senha**: Senha do usuário (mínimo 6 caracteres)
    - **id_perfil_acesso**: ID do perfil de acesso
    - **empresa_origem**: ID da empresa de origem (opcional)
    - **contato**: Contato do usuário (opcional)
    """
    try:
        service = UsuarioService(db)
        usuario = service.criar_usuario(usuario_data)
        return usuario
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    credenciais: UsuarioLogin,
    db: Session = Depends(get_db)
):
    """
    Autentica um usuário e retorna um token JWT
    
    - **login**: Login do usuário
    - **senha**: Senha do usuário
    """
    service = UsuarioService(db)
    usuario = service.autenticar_usuario(credenciais.login, credenciais.senha)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Criar token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = SecurityService.create_access_token(
        data={"sub": usuario.login, "id": usuario.id_usuario},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": usuario
    }


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obter_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """Obtém informações de um usuário específico"""
    service = UsuarioService(db)
    usuario = service.obter_usuario_por_id(usuario_id)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return usuario


@router.get("/", response_model=list[UsuarioResponse])
async def listar_usuarios(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Lista todos os usuários com paginação"""
    service = UsuarioService(db)
    usuarios = service.listar_usuarios(skip=skip, limit=limit)
    return usuarios


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def atualizar_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um usuário existente"""
    try:
        service = UsuarioService(db)
        usuario = service.atualizar_usuario(usuario_id, usuario_data)
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        return usuario
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """Deleta um usuário"""
    try:
        service = UsuarioService(db)
        sucesso = service.deletar_usuario(usuario_id)
        
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
