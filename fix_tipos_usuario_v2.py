#!/usr/bin/env python3
"""
Script para adicionar coluna 'chave' usando a conexão do projeto
"""

import sys
sys.path.insert(0, '/Users/adsow/Desktop/trabalho de bd terceiro')

from app.database.connection import SessionLocal
from app.models.lookups import LuTiposUsuario
from sqlalchemy import text

def main():
    """Executa a migração"""
    db = SessionLocal()
    
    try:
        print("\n📝 Iniciando migração de lu_tipos_usuario...\n")
        
        # Verificar se coluna já existe
        try:
            # Tentar descrever a tabela
            result = db.execute(text("DESCRIBE lu_tipos_usuario"))
            colunas = [row[0] for row in result.fetchall()]
            
            if 'chave' not in colunas:
                print("Adicionando coluna 'chave'...")
                db.execute(text("ALTER TABLE lu_tipos_usuario ADD COLUMN chave VARCHAR(50) NOT NULL UNIQUE AFTER id"))
                db.commit()
                print("✓ Coluna 'chave' adicionada")
            else:
                print("✓ Coluna 'chave' já existe")
        except Exception as e:
            print(f"⚠️ Ao verificar/adicionar coluna: {e}")
        
        # Limpar dados antigos (respeitando foreign keys)
        print("\nLimpando dados antigos...")
        
        # Desabilitar checks temporariamente
        db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        
        # Deletar tudo que referencia tipos de usuário
        db.execute(text("DELETE FROM acessos_veiculares"))
        db.execute(text("DELETE FROM acessos_pessoais"))
        db.execute(text("DELETE FROM usuarios"))
        db.execute(text("DELETE FROM lu_tipos_usuario"))
        
        # Reabilitar checks
        db.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        
        db.commit()
        print("✓ Dados antigos removidos")
        
        # Inserir dados corretos
        print("Inserindo novos tipos de usuário...")
        db.execute(text("""
            INSERT INTO lu_tipos_usuario (chave, descricao) VALUES
            ('funcionario', 'Funcionário'),
            ('terceiro', 'Terceiro'),
            ('visitante', 'Visitante'),
            ('admin', 'Administrador'),
            ('seguranca', 'Segurança'),
            ('operador', 'Operador')
        """))
        db.commit()
        print("✓ Dados inseridos")
        
        # Verificar dados
        result = db.execute(text("SELECT id, chave, descricao FROM lu_tipos_usuario ORDER BY id"))
        print("\n📋 Tipos de Usuário cadastrados:\n")
        for row in result.fetchall():
            print(f"  ID: {row[0]:2d} | Chave: {row[1]:12s} | Nome: {row[2]}")
        
        print("\n✅ Migração concluída com sucesso!\n")
        
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
