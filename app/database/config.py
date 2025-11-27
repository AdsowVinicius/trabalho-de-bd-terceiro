from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação"""
    database_url: str = "mysql+pymysql://root:admin@127.0.0.1:3306/controle_acesso"
    secret_key: str = "sua_chave_secreta_muito_segura_aqui"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False  # Permite ler DATABASE_URL como database_url


settings = Settings()
