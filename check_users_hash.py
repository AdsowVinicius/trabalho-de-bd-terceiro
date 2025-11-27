"""
Diagnostic script to check user password hashes in the database.
"""
from app.database.connection import SessionLocal
from app.models.usuario import Usuario

db = SessionLocal()
try:
    usuarios = db.query(Usuario).limit(5).all()
    print(f"\nFound {len(usuarios)} users in database:\n")
    for user in usuarios:
        print(f"ID: {user.id}")
        print(f"  Login: {user.login}")
        print(f"  Senha Hash (first 50 chars): {user.senha_hash[:50] if user.senha_hash else 'NULL'}")
        print(f"  Hash length: {len(user.senha_hash) if user.senha_hash else 0}")
        print(f"  Is hash valid format? {user.senha_hash.startswith('$') if user.senha_hash else False}")
        print()
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
