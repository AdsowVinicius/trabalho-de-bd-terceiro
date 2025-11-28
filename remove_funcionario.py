#!/usr/bin/env python3
"""
Script para remover tipo de usuário 'funcionario' do banco
"""

import sys
sys.path.insert(0, '/Users/adsow/Desktop/trabalho de bd terceiro')

from app.database.connection import SessionLocal
from sqlalchemy import text

def main():
    """Remove funcionário do banco"""
    db = SessionLocal()
    
    try:
        print("\n📝 Removendo tipo 'funcionário'...\n")
        
        # Desabilitar checks temporariamente
        db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        
        # Deletar o tipo funcionário
        db.execute(text("DELETE FROM lu_tipos_usuario WHERE chave = 'funcionario'"))
        
        # Reabilitar checks
        db.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        
        db.commit()
        print("✓ Tipo 'funcionário' removido")
        
        # Verificar dados restantes
        result = db.execute(text("SELECT id, chave, descricao FROM lu_tipos_usuario ORDER BY id"))
        print("\n📋 Tipos de Usuário restantes:\n")
        for row in result.fetchall():
            print(f"  ID: {row[0]:2d} | Chave: {row[1]:12s} | Nome: {row[2]}")
        
        print("\n✅ Operação concluída!\n")
        
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
