#!/usr/bin/env python3
"""
Script para adicionar coluna 'chave' na tabela lu_tipos_usuario e popular os dados
"""

from sqlalchemy import text, create_engine

def conectar_banco():
    """Conecta ao banco de dados usando SQLAlchemy"""
    try:
        # Tentar diferentes URLs de conexão
        urls = [
            "mysql+pymysql://root:admin@127.0.0.1:3306/controle_acesso",
            "mysql+pymysql://root:@127.0.0.1:3306/controle_acesso",
            "mysql+pymysql://root@127.0.0.1:3306/controle_acesso",
        ]
        
        engine = None
        for url in urls:
            try:
                engine = create_engine(url)
                connection = engine.connect()
                print(f"✓ Conectado ao banco com: {url}")
                return engine, connection
            except Exception as e:
                print(f"  Tentativa falhou: {str(e)[:50]}...")
                continue
        
        if not engine:
            raise Exception("Nenhuma URL de conexão funcionou")
        
    except Exception as e:
        print(f"✗ Erro ao conectar: {e}")
        return None, None

def executar_query(connection, query, descricao=""):
    """Executa uma query no banco"""
    try:
        connection.execute(text(query))
        connection.commit()
        print(f"✓ {descricao}")
        return True
    except Exception as e:
        print(f"✗ Erro em '{descricao}': {e}")
        connection.rollback()
        return False

def main():
    engine, connection = conectar_banco()
    if not connection:
        return
    
    try:
        print("\n📝 Iniciando migração de lu_tipos_usuario...\n")
        
        # Verificar se coluna já existe
        try:
            result = connection.execute(text("DESCRIBE lu_tipos_usuario"))
            colunas = [row[0] for row in result.fetchall()]
            
            if 'chave' not in colunas:
                # Adicionar coluna chave
                executar_query(
                    connection,
                    "ALTER TABLE lu_tipos_usuario ADD COLUMN chave VARCHAR(50) NOT NULL UNIQUE AFTER id",
                    "Coluna 'chave' adicionada"
                )
            else:
                print("✓ Coluna 'chave' já existe")
        except Exception as e:
            print(f"⚠️ Aviso ao verificar colunas: {e}")
        
        # Limpar dados antigos
        print("\nLimpando dados antigos...")
        try:
            connection.execute(text("DELETE FROM lu_tipos_usuario"))
            connection.commit()
            print("✓ Tabela lu_tipos_usuario limpa")
        except Exception as e:
            print(f"⚠️ Erro ao limpar (pode estar vazia): {e}")
            connection.rollback()
        
        # Inserir dados corretos
        executar_query(
            connection,
            """INSERT INTO lu_tipos_usuario (chave, nome) VALUES
              ('funcionario', 'Funcionário'),
              ('terceiro', 'Terceiro'),
              ('visitante', 'Visitante'),
              ('admin', 'Administrador'),
              ('seguranca', 'Segurança'),
              ('operador', 'Operador')""",
            "Dados de tipos de usuário inseridos"
        )
        
        # Verificar dados inseridos
        result = connection.execute(text("SELECT id, chave, nome FROM lu_tipos_usuario"))
        print("\n📋 Tipos de Usuário cadastrados:\n")
        for row in result.fetchall():
            print(f"  ID: {row[0]} | Chave: {row[1]} | Nome: {row[2]}")
        
        print("\n✅ Migração concluída com sucesso!\n")
        
    except Exception as e:
        print(f"✗ Erro geral: {e}")
    finally:
        if connection:
            connection.close()
        if engine:
            engine.dispose()
            print("Conexão encerrada")

if __name__ == "__main__":
    main()

