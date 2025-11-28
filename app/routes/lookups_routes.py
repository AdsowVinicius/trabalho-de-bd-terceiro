from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from ..database.connection import get_db

router = APIRouter(prefix="/lookups", tags=["Lookups"])


def _safe_lookup_list(db: Session, table_name: str, id_col: str = "id", name_col: str = None) -> List[dict]:
    """Run a safe SQL that selects id and a name column.

    If name_col is provided, uses that. Otherwise detects which name column exists
    (nome, descricao, nome_empresa, label, valor, name, titulo) and uses that.
    Falls back gracefully if no suitable column exists.
    Returns an empty list on any error to keep the frontend resilient.
    """
    try:
        # If name column not provided, detect it
        if not name_col:
            # List of possible name column names in order of preference
            possible_columns = ["nome", "descricao", "nome_empresa", "label", "valor", "name", "titulo"]
            
            # Get actual columns in the table
            info_sql = text(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = DATABASE()")
            columns = [r[0] for r in db.execute(info_sql).fetchall()]
            
            # Find the first matching column
            for col in possible_columns:
                if col in columns:
                    name_col = col
                    break
        
        # Se é tabela de tipos de usuário, incluir a coluna 'chave'
        if table_name == "lu_tipos_usuario":
            sql = text(f"SELECT {id_col} as id, {name_col} as nome, chave FROM {table_name} ORDER BY {id_col}")
            res = db.execute(sql).mappings().all()
            return [{"id": r["id"], "nome": (r["nome"] or ""), "chave": r["chave"]} for r in res]
        
        # If no suitable column found, return just IDs
        if not name_col:
            sql = text(f"SELECT {id_col} as id FROM {table_name} ORDER BY {id_col}")
            res = db.execute(sql).mappings().all()
            return [{"id": r["id"], "nome": ""} for r in res]
        
        # Use the detected or provided column
        sql = text(f"SELECT {id_col} as id, {name_col} as nome FROM {table_name} ORDER BY {id_col}")
        res = db.execute(sql).mappings().all()
        return [{"id": r["id"], "nome": (r["nome"] or "")} for r in res]
    except Exception as e:
        # Do not expose DB internals to the frontend; return empty list instead.
        print(f"Erro em _safe_lookup_list: {e}")
        return []


@router.get("/perfis", response_model=List[dict])
def get_perfis(db: Session = Depends(get_db)):
    return _safe_lookup_list(db, "lu_perfis_acesso")


@router.get("/tipos-usuario", response_model=List[dict])
def get_tipos_usuario(db: Session = Depends(get_db)):
    return _safe_lookup_list(db, "lu_tipos_usuario")


@router.get("/tipos-empresa", response_model=List[dict])
def get_tipos_empresa(db: Session = Depends(get_db)):
    return _safe_lookup_list(db, "lu_tipos_empresa")


@router.get("/tipos-servico", response_model=List[dict])
def get_tipos_servico(db: Session = Depends(get_db)):
    return _safe_lookup_list(db, "lu_tipos_servico")


@router.get("/empresas", response_model=List[dict])
def get_empresas(db: Session = Depends(get_db)):
    """Get list of companies (empresas)"""
    return _safe_lookup_list(db, "empresas", id_col="id_empresa", name_col="nome_empresa")


@router.get("/veiculos", response_model=List[dict])
def get_veiculos(db: Session = Depends(get_db)):
    """Get list of vehicles with id, placa, ano, modelo and id_responsavel"""
    try:
        sql = text("""
            SELECT id_veiculo as id, placa, ano, modelo, id_responsavel
            FROM veiculos 
            ORDER BY placa
        """)
        res = db.execute(sql).mappings().all()
        return [{"id": r["id"], "placa": r["placa"], "ano": r["ano"], "modelo": r["modelo"], "id_responsavel": r["id_responsavel"]} for r in res]
    except Exception:
        return []


@router.get("/responsaveis", response_model=List[dict])
def get_responsaveis(db: Session = Depends(get_db)):
    """Get list of responsible users (motoristas/condutores)"""
    try:
        sql = text("""
            SELECT id_usuario as id, nome, documento, login 
            FROM usuarios 
            WHERE ativo = 1 
            ORDER BY nome
        """)
        res = db.execute(sql).mappings().all()
        return [{"id": r["id"], "nome": r["nome"], "documento": r["documento"], "login": r["login"]} for r in res]
    except Exception:
        return []


@router.get("/transportadoras", response_model=List[dict])
def get_transportadoras(db: Session = Depends(get_db)):
    """Get list of companies that are transporters"""
    try:
        sql = text("""
            SELECT id_empresa as id, nome_empresa as nome, cnpj 
            FROM empresas 
            WHERE id_tipo_empresa = (SELECT id FROM lu_tipos_empresa WHERE chave = 'transportadora' LIMIT 1)
            ORDER BY nome_empresa
        """)
        res = db.execute(sql).mappings().all()
        if not res:
            # Fallback: return all companies if no transportadora type found
            sql = text("""
                SELECT id_empresa as id, nome_empresa as nome, cnpj 
                FROM empresas 
                ORDER BY nome_empresa
            """)
            res = db.execute(sql).mappings().all()
        return [{"id": r["id"], "nome": r["nome"], "cnpj": r["cnpj"]} for r in res]
    except Exception:
        return []

