from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional
from ..database.config import settings

# Contexto para hash de senha
# Support both the newer `pbkdf2_sha256` for new hashes and `bcrypt`
# so existing user records hashed with bcrypt can still be verified.
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")


class SecurityService:
    """Serviço de segurança para autenticação e criptografia"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Criptografa uma senha usando o esquema padrão (`pbkdf2_sha256`).

        Args:
            password: Senha em texto plano

        Returns:
            Senha criptografada
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se uma senha corresponde ao hash
        
        Args:
            plain_password: Senha em texto plano
            hashed_password: Senha criptografada
            
        Returns:
            True se as senhas correspondem, False caso contrário
        """
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            # If hash format is unrecognized (e.g., plain MD5/SHA256), return False
            # This prevents "UnknownHashError" from crashing the endpoint
            return False
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Cria um token JWT
        
        Args:
            data: Dados a serem incluídos no token
            expires_delta: Tempo de expiração do token
            
        Returns:
            Token JWT codificado
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.access_token_expire_minutes
            )
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        """
        Decodifica um token JWT
        
        Args:
            token: Token JWT
            
        Returns:
            Dados do token ou None se inválido
        """
        try:
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.algorithm]
            )
            return payload
        except JWTError:
            return None
