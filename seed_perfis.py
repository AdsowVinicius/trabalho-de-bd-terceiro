"""
Script para inserir ou atualizar perfis de acesso na tabela lu_perfis_acesso.
"""
from app.database.connection import SessionLocal
from sqlalchemy import text

db = SessionLocal()
try:
    # Perfis que devem existir
    perfis = [
        (1, 'Porteiro'),
        (2, 'Funcionário'),
        (3, 'Administrador'),
        (4, 'Segurança'),
    ]
    
    # Inserir ou atualizar os perfis
    for perfil_id, perfil_nome in perfis:
        # Verificar se já existe
        result = db.execute(text(f"SELECT id FROM lu_perfis_acesso WHERE id = {perfil_id}")).fetchone()
        
        if result:
            # Atualizar
            db.execute(text(f"UPDATE lu_perfis_acesso SET nome = '{perfil_nome}' WHERE id = {perfil_id}"))
            print(f"✓ Atualizado: Perfil ID {perfil_id} -> {perfil_nome}")
        else:
            # Inserir
            db.execute(text(f"INSERT INTO lu_perfis_acesso (id, nome) VALUES ({perfil_id}, '{perfil_nome}')"))
            print(f"✓ Inserido: Perfil ID {perfil_id} -> {perfil_nome}")
    
    db.commit()
    print("\n✓ Perfis sincronizados com sucesso!")
    
except Exception as e:
    print(f"✗ Erro: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
