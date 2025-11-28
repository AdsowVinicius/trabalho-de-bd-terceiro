from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..database import get_db

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/acessos-pessoais-detalhado")
async def acessos_pessoais_detalhado(db: Session = Depends(get_db)):
    """Retorna os acessos pessoais detalhados via VIEW"""
    try:
        query = text("""
            SELECT 
                id_acesso_pessoal,
                data_registro,
                id_usuario,
                nome_usuario,
                documento_cadastrado,
                tipo_acesso,
                empresa_visitada,
                motivo_visita,
                hora_entrada,
                hora_saida,
                observacao
            FROM vw_acessos_pessoais_detalhado
            ORDER BY data_registro DESC
        """)
        result = db.execute(query)
        rows = result.fetchall()
        
        # Converter para lista de dicts
        dados = []
        for row in rows:
            dados.append({
                "id_acesso_pessoal": row[0],
                "data_registro": row[1],
                "id_usuario": row[2],
                "nome_usuario": row[3],
                "documento_cadastrado": row[4],
                "tipo_acesso": row[5],
                "empresa_visitada": row[6],
                "motivo_visita": row[7],
                "hora_entrada": row[8],
                "hora_saida": row[9],
                "observacao": row[10]
            })
        
        return {"total": len(dados), "dados": dados}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar dados: {str(e)}"
        )


@router.get("/acessos-veiculares-detalhado")
async def acessos_veiculares_detalhado(db: Session = Depends(get_db)):
    """Retorna os acessos veiculares detalhados via VIEW"""
    try:
        query = text("""
            SELECT 
                id_acesso_veiculo,
                data_registro,
                id_veiculo,
                placa,
                modelo,
                ano_cadastrado,
                id_responsavel,
                nome_responsavel,
                transportadora,
                tipo_servico,
                nota_fiscal_entrada,
                nota_fiscal_saida,
                hora_entrada,
                hora_saida,
                observacao
            FROM vw_acessos_veiculares_detalhado
            ORDER BY data_registro DESC
        """)
        result = db.execute(query)
        rows = result.fetchall()
        
        # Converter para lista de dicts
        dados = []
        for row in rows:
            dados.append({
                "id_acesso_veiculo": row[0],
                "data_registro": row[1],
                "id_veiculo": row[2],
                "placa": row[3],
                "modelo": row[4],
                "ano_cadastrado": row[5],
                "id_responsavel": row[6],
                "nome_responsavel": row[7],
                "transportadora": row[8],
                "tipo_servico": row[9],
                "nota_fiscal_entrada": row[10],
                "nota_fiscal_saida": row[11],
                "hora_entrada": row[12],
                "hora_saida": row[13],
                "observacao": row[14]
            })
        
        return {"total": len(dados), "dados": dados}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar dados: {str(e)}"
        )


@router.get("/visitantes-ativos")
async def visitantes_ativos(db: Session = Depends(get_db)):
    """Retorna visitantes atualmente dentro do prédio"""
    try:
        query = text("""
            SELECT 
                id_acesso_pessoal,
                nome,
                documento,
                hora_entrada,
                motivo_visita,
                empresa_visitada
            FROM vw_visitantes_ativos
            ORDER BY hora_entrada DESC
        """)
        result = db.execute(query)
        rows = result.fetchall()
        
        # Converter para lista de dicts
        dados = []
        for row in rows:
            dados.append({
                "id_acesso_pessoal": row[0],
                "nome": row[1],
                "documento": row[2],
                "hora_entrada": row[3],
                "motivo_visita": row[4],
                "empresa_visitada": row[5]
            })
        
        return {"total": len(dados), "dados": dados}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar dados: {str(e)}"
        )


@router.get("/veiculos-ativos")
async def veiculos_ativos(db: Session = Depends(get_db)):
    """Retorna veículos atualmente dentro do pátio"""
    try:
        query = text("""
            SELECT 
                id_acesso_veiculo,
                placa,
                modelo,
                motorista,
                hora_entrada,
                id_tipo_servico
            FROM vw_veiculos_ativos
            ORDER BY hora_entrada DESC
        """)
        result = db.execute(query)
        rows = result.fetchall()
        
        # Converter para lista de dicts
        dados = []
        for row in rows:
            dados.append({
                "id_acesso_veiculo": row[0],
                "placa": row[1],
                "modelo": row[2],
                "motorista": row[3],
                "hora_entrada": row[4],
                "id_tipo_servico": row[5]
            })
        
        return {"total": len(dados), "dados": dados}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar dados: {str(e)}"
        )
