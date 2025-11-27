#!/usr/bin/env python
"""
Script de diagnóstico para verificar banco de dados
"""

import sys
import mysql.connector
from mysql.connector import Error

def check_mysql_connection():
    """Verifica conexão com MySQL"""
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            port=3307,
            user='root',
            password='admin'
        )
        if conn.is_connected():
            print("✅ MySQL está conectado com sucesso!")
            cursor = conn.cursor()
            
            # Listar bancos de dados
            cursor.execute("SHOW DATABASES;")
            databases = cursor.fetchall()
            print("\n📊 Bancos de dados disponíveis:")
            for db in databases:
                print(f"   - {db[0]}")
            
            # Verificar se controle_acesso existe
            if any(db[0] == 'controle_acesso' for db in databases):
                print("\n✅ Banco 'controle_acesso' existe!")
                
                # Conectar ao banco e listar tabelas
                conn2 = mysql.connector.connect(
                    host='127.0.0.1',
                    port=3307,
                    user='root',
                    password='admin',
                    database='controle_acesso'
                )
                cursor2 = conn2.cursor()
                cursor2.execute("SHOW TABLES;")
                tables = cursor2.fetchall()
                
                if tables:
                    print(f"\n📋 Tabelas ({len(tables)} encontradas):")
                    for table in tables:
                        print(f"   - {table[0]}")
                else:
                    print("\n⚠️  Banco 'controle_acesso' existe mas não tem tabelas!")
                    print("    Execute os scripts SQL em querys/")
                
                conn2.close()
            else:
                print("\n❌ Banco 'controle_acesso' NÃO EXISTE!")
                print("\nExecute:")
                print("   mysql -u root -p -e \"CREATE DATABASE controle_acesso CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci\"")
                print("   mysql -u root -p controle_acesso < \"querys/Query 1.sql\"")
                print("   mysql -u root -p controle_acesso < \"querys/Query 2.sql\"")
            
            cursor.close()
            conn.close()
    
    except Error as e:
        print(f"❌ Erro ao conectar com MySQL: {e}")
        print("\n📝 Verificações:")
        print("   1. MySQL/MariaDB está rodando?")
        print("      Comando: net start MySQL80 (Windows Admin)")
        print("   2. Porta 3306 está correta?")
        print("   3. Usuário 'root' com senha 'admin' existe?")
        print("\nDica: Verifique arquivo .env para credenciais corretas")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("DIAGNÓSTICO DE BANCO DE DADOS")
    print("=" * 60)
    check_mysql_connection()
    print("\n" + "=" * 60)
    print("✅ Diagnóstico concluído!")
    print("=" * 60)
