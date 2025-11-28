from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from ..models.usuario import Usuario
from ..schemas.usuario_schema import UsuarioCreate, UsuarioUpdate
from ..utils.security import SecurityService
from datetime import timedelta
import random
import string


class UsuarioService:
    """Serviço de negócio para operações de usuários"""
    
    def __init__(self, db: Session):
        """
        Inicializa o serviço de usuários
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.security_service = SecurityService()
    
    def _gerar_login_aleatorio(self) -> str:
        """Gera um login aleatório único"""
        while True:
            login = 'user_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            usuario_existente = self.db.query(Usuario).filter(Usuario.login == login).first()
            if not usuario_existente:
                return login
    
    def _gerar_senha_aleatoria(self) -> str:
        """Gera uma senha aleatória segura"""
        chars = string.ascii_letters + string.digits + '!@#$%'
        return ''.join(random.choices(chars, k=12))
    
    def criar_usuario(self, usuario_data: UsuarioCreate) -> Usuario:
        """
        Cria um novo usuário
        
        Args:
            usuario_data: Dados do usuário a ser criado
            
        Returns:
            Usuário criado
            
        Raises:
            ValueError: Se o login ou documento já existem
        """
        # Verificar se documento já existe
        usuario_existente = self.db.query(Usuario).filter(
            Usuario.documento == usuario_data.documento
        ).first()
        
        if usuario_existente:
            raise ValueError("Documento já cadastrado")
        
        # Obter o tipo de usuário para verificar se é interno
        from ..models.lookups import LuTiposUsuario
        tipo_usuario = self.db.query(LuTiposUsuario).filter(
            LuTiposUsuario.id == usuario_data.id_tipo_usuario
        ).first()
        
        # Tipos internos que REQUEREM login/senha/perfil: admin, seguranca, operador
        tipos_internos = ['admin', 'seguranca', 'operador']
        eh_interno = tipo_usuario and tipo_usuario.chave in tipos_internos
        
        # Se for interno, login e senha são obrigatórios
        if eh_interno:
            if not usuario_data.login or not usuario_data.senha:
                raise ValueError("Login e senha são obrigatórios para usuários internos")
            if not usuario_data.id_perfil_acesso:
                raise ValueError("Perfil de acesso é obrigatório para usuários internos")
        else:
            # Terceiro, Visitante não devem ter login, senha ou perfil
            usuario_data.login = None
            usuario_data.senha = None
            usuario_data.id_perfil_acesso = None
        
        # Verificar se login já existe (apenas se houver login)
        if usuario_data.login:
            usuario_existente = self.db.query(Usuario).filter(
                Usuario.login == usuario_data.login
            ).first()
            
            if usuario_existente:
                raise ValueError("Login já cadastrado")
        
        # Hash da senha (apenas se houver senha)
        senha_hash = None
        if usuario_data.senha:
            senha_hash = self.security_service.hash_password(usuario_data.senha)
        
        # Criar novo usuário
        novo_usuario = Usuario(
            nome=usuario_data.nome,
            documento=usuario_data.documento,
            id_tipo_usuario=usuario_data.id_tipo_usuario,
            login=usuario_data.login,
            senha_hash=senha_hash,
            id_perfil_acesso=usuario_data.id_perfil_acesso,
            empresa_origem=usuario_data.empresa_origem,
            contato=usuario_data.contato,
            ativo=usuario_data.ativo
        )
        
        try:
            self.db.add(novo_usuario)
            self.db.commit()
            self.db.refresh(novo_usuario)
            return novo_usuario
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao criar usuário - dados duplicados ou inválidos")
    
    def obter_usuario_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """
        Obtém um usuário pelo ID
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Usuário encontrado ou None
        """
        return self.db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    
    def obter_usuario_por_login(self, login: str) -> Optional[Usuario]:
        """
        Obtém um usuário pelo login
        
        Args:
            login: Login do usuário
            
        Returns:
            Usuário encontrado ou None
        """
        return self.db.query(Usuario).filter(Usuario.login == login).first()
    
    def listar_usuarios(self, skip: int = 0, limit: int = 10) -> List[Usuario]:
        """
        Lista todos os usuários com paginação
        
        Args:
            skip: Número de registros a pular
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de usuários
        """
        return self.db.query(Usuario).offset(skip).limit(limit).all()
    
    def atualizar_usuario(self, usuario_id: int, usuario_data: UsuarioUpdate) -> Optional[Usuario]:
        """
        Atualiza um usuário existente
        
        Args:
            usuario_id: ID do usuário
            usuario_data: Dados a serem atualizados
            
        Returns:
            Usuário atualizado ou None se não encontrado
        """
        usuario = self.obter_usuario_por_id(usuario_id)
        
        if not usuario:
            return None
        
        # Determinar se é usuário interno pela chave
        from ..models.lookups import LuTiposUsuario
        tipos_internos = ['admin', 'seguranca', 'operador']
        
        # Se houver mudança de tipo, usar o novo tipo
        tipo_id_para_verificar = usuario_data.id_tipo_usuario if hasattr(usuario_data, 'id_tipo_usuario') and usuario_data.id_tipo_usuario else usuario.id_tipo_usuario
        
        tipo_usuario = self.db.query(LuTiposUsuario).filter(
            LuTiposUsuario.id == tipo_id_para_verificar
        ).first()
        
        eh_interno = tipo_usuario and tipo_usuario.chave in tipos_internos
        
        # Atualizar tipo de usuário se informado
        if hasattr(usuario_data, 'id_tipo_usuario') and usuario_data.id_tipo_usuario is not None:
            usuario.id_tipo_usuario = usuario_data.id_tipo_usuario
        
        # Atualizar campos básicos
        if usuario_data.nome is not None:
            usuario.nome = usuario_data.nome
        if usuario_data.contato is not None:
            usuario.contato = usuario_data.contato
        if usuario_data.ativo is not None:
            usuario.ativo = usuario_data.ativo
        if usuario_data.empresa_origem is not None:
            usuario.empresa_origem = usuario_data.empresa_origem
        
        # Atualizar campos de acesso (login, senha, perfil) conforme tipo
        if eh_interno:
            # Usuário interno pode ter login, senha e perfil
            if hasattr(usuario_data, 'login') and usuario_data.login is not None:
                usuario.login = usuario_data.login
            if hasattr(usuario_data, 'senha') and usuario_data.senha is not None:
                usuario.senha_hash = self.security_service.hash_password(usuario_data.senha)
            if hasattr(usuario_data, 'id_perfil_acesso') and usuario_data.id_perfil_acesso is not None:
                usuario.id_perfil_acesso = usuario_data.id_perfil_acesso
        else:
            # Usuário externo não deve ter login, senha ou perfil
            usuario.login = None
            usuario.senha_hash = None
            usuario.id_perfil_acesso = None
        
        try:
            self.db.commit()
            self.db.refresh(usuario)
            return usuario
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao atualizar usuário - dados duplicados ou inválidos")
    
    def deletar_usuario(self, usuario_id: int) -> bool:
        """
        Deleta um usuário
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            True se deletado, False se não encontrado
        """
        usuario = self.obter_usuario_por_id(usuario_id)
        
        if not usuario:
            return False
        
        try:
            self.db.delete(usuario)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao deletar usuário - pode ter registros relacionados")
    
    def autenticar_usuario(self, login: str, senha: str) -> Optional[Usuario]:
        """
        Autentica um usuário com login e senha
        
        Args:
            login: Login do usuário
            senha: Senha em texto plano
            
        Returns:
            Usuário autenticado ou None
        """
        usuario = self.obter_usuario_por_login(login)
        
        if not usuario:
            return None
        
        if not self.security_service.verify_password(senha, usuario.senha_hash):
            return None
        
        if not usuario.ativo:
            return None
        
        return usuario
