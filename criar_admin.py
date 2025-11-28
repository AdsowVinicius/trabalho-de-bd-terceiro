"""
Script para criar um usuário admin no banco de dados
"""

import pymysql
from passlib.context import CryptContext
from datetime import datetime

# Configuração do banco (ajuste conforme necessário)
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "admin"
DB_NAME = "controle_acesso"
DB_PORT = 3307

# Context para hash de senha
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Dados do admin
ADMIN_NOME = "Adsow Admin"
ADMIN_DOCUMENTO = "00000000003"  # Mude o documento
ADMIN_LOGIN = "adsow"  # Mude o login
ADMIN_SENHA = "adsow123" # MUDE ISSO!
ADMIN_TIPO_USUARIO = 10  # ID do tipo "admin" no banco
ADMIN_PERFIL = None  # Opcional - pode deixar NULL

try:
    # Conecta ao banco
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
    cursor = conn.cursor()
    # Hash a senha
    senha_hash = pwd_context.hash(ADMIN_SENHA)
    
    # SQL para inserir
    sql = """
    INSERT INTO usuarios 
    (nome, documento, id_tipo_usuario, login, senha_hash, id_perfil_acesso, ativo, data_cadastro)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    valores = (
        ADMIN_NOME,
        ADMIN_DOCUMENTO,
        ADMIN_TIPO_USUARIO,
        ADMIN_LOGIN,
        senha_hash,
        ADMIN_PERFIL,
        True,
        datetime.now()
    )
    
    cursor.execute(sql, valores)
    conn.commit()
    
    print("✅ Admin criado com sucesso!")
    print(f"Login: {ADMIN_LOGIN}")
    print(f"Senha: {ADMIN_SENHA}")
    print(f"ID do usuário: {cursor.lastrowid}")
    
except pymysql.err.IntegrityError as e:
    print(f"❌ Erro: Usuário/documento já existe: {e}")
except Exception as e:
    print(f"❌ Erro ao criar admin: {e}")
finally:
    cursor.close()
    conn.close()
