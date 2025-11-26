from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação"""
    database_url: str = "mysql+pymysql://root:@localhost:3307/controle_acesso"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"


settings = Settings()
