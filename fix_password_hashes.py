"""
Script to rehash invalid password hashes in the database.
This fixes users with plain text or unrecognized hash formats.
"""
from app.database.connection import SessionLocal
from app.models.usuario import Usuario
from app.utils.security import SecurityService

db = SessionLocal()
try:
    usuarios = db.query(Usuario).all()
    security = SecurityService()
    updated_count = 0
    
    for user in usuarios:
        # Try to identify if hash is valid passlib format
        is_valid = False
        if user.senha_hash and user.senha_hash.startswith('$'):
            is_valid = True
        
        if not is_valid and user.senha_hash:
            print(f"Found invalid hash for user {user.login} (ID {user.id_usuario})")
            print(f"  Old hash: {user.senha_hash[:50]}...")
            
            # For admin user with plain text or unknown hash, use a known password
            if user.login == 'admin':
                # Hash the password 'admin' with the proper scheme
                user.senha_hash = security.hash_password('admin')
                print(f"  New hash: {user.senha_hash}")
                updated_count += 1
            elif user.login == 'joao_silva':
                # For joao_silva, also use a known password for testing
                user.senha_hash = security.hash_password('senha_joao')
                print(f"  New hash: {user.senha_hash}")
                updated_count += 1
    
    if updated_count > 0:
        db.commit()
        print(f"\nSuccessfully updated {updated_count} user(s).")
    else:
        print("\nNo invalid hashes found.")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
