from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from ..models.acesso_pessoal import AcessoPessoal
from ..schemas.acesso_pessoal_schema import AcessoPessoalCreate, AcessoPessoalUpdate
from datetime import datetime


class AcessoPessoalService:
    """Serviço de negócio para operações de acessos pessoais"""
    
    def __init__(self, db: Session):
        """
        Inicializa o serviço de acessos pessoais
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db
    
    def criar_acesso(self, acesso_data: AcessoPessoalCreate) -> AcessoPessoal:
        """
        Registra uma entrada pessoal
        
        Args:
            acesso_data: Dados do acesso a ser criado
            
        Returns:
            Acesso pessoal criado
        """
        novo_acesso = AcessoPessoal(
            id_usuario=acesso_data.id_usuario,
            id_tipo_acesso=acesso_data.id_tipo_acesso,
            id_empresa_visitada=acesso_data.id_empresa_visitada,
            motivo_visita=acesso_data.motivo_visita,
            observacao=acesso_data.observacao
        )
        
        try:
            self.db.add(novo_acesso)
            self.db.commit()
            self.db.refresh(novo_acesso)
            return novo_acesso
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao registrar acesso")
    
    def obter_acesso_por_id(self, acesso_id: int) -> Optional[AcessoPessoal]:
        """
        Obtém um acesso pelo ID
        
        Args:
            acesso_id: ID do acesso
            
        Returns:
            Acesso encontrado ou None
        """
        return self.db.query(AcessoPessoal).filter(
            AcessoPessoal.id_acesso_pessoal == acesso_id
        ).first()
    
    def listar_acessos(self, skip: int = 0, limit: int = 10) -> List[AcessoPessoal]:
        """
        Lista todos os acessos com paginação
        
        Args:
            skip: Número de registros a pular
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de acessos
        """
        return self.db.query(AcessoPessoal).offset(skip).limit(limit).all()
    
    def listar_acessos_por_usuario(self, usuario_id: int) -> List[AcessoPessoal]:
        """
        Lista acessos de um usuário
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Lista de acessos
        """
        return self.db.query(AcessoPessoal).filter(
            AcessoPessoal.id_usuario == usuario_id
        ).all()
    
    def listar_visitantes_ativos(self) -> List[AcessoPessoal]:
        """
        Lista visitantes atualmente dentro (sem hora_saida)
        
        Returns:
            Lista de acessos ativos
        """
        return self.db.query(AcessoPessoal).filter(
            AcessoPessoal.hora_saida.is_(None)
        ).all()
    
    def registrar_saida(self, acesso_id: int, acesso_data: AcessoPessoalUpdate) -> Optional[AcessoPessoal]:
        """
        Registra a saída de uma pessoa
        
        Args:
            acesso_id: ID do acesso
            acesso_data: Dados de saída
            
        Returns:
            Acesso atualizado ou None se não encontrado
        """
        acesso = self.obter_acesso_por_id(acesso_id)
        
        if not acesso:
            return None
        
        # Se não foi fornecida hora_saida, usar agora
        if acesso_data.hora_saida is None:
            acesso.hora_saida = datetime.utcnow()
        else:
            acesso.hora_saida = acesso_data.hora_saida
        
        if acesso_data.observacao is not None:
            acesso.observacao = acesso_data.observacao
        
        if acesso_data.motivo_visita is not None:
            acesso.motivo_visita = acesso_data.motivo_visita
        
        try:
            self.db.commit()
            self.db.refresh(acesso)
            return acesso
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao registrar saída")
    
    def atualizar_acesso(self, acesso_id: int, acesso_data: AcessoPessoalUpdate) -> Optional[AcessoPessoal]:
        """
        Atualiza um acesso existente
        
        Args:
            acesso_id: ID do acesso
            acesso_data: Dados a serem atualizados
            
        Returns:
            Acesso atualizado ou None se não encontrado
        """
        acesso = self.obter_acesso_por_id(acesso_id)
        
        if not acesso:
            return None
        
        if acesso_data.motivo_visita is not None:
            acesso.motivo_visita = acesso_data.motivo_visita
        if acesso_data.observacao is not None:
            acesso.observacao = acesso_data.observacao
        if acesso_data.hora_saida is not None:
            acesso.hora_saida = acesso_data.hora_saida
        
        try:
            self.db.commit()
            self.db.refresh(acesso)
            return acesso
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao atualizar acesso")
    
    def deletar_acesso(self, acesso_id: int) -> bool:
        """
        Deleta um acesso
        
        Args:
            acesso_id: ID do acesso
            
        Returns:
            True se deletado, False se não encontrado
        """
        acesso = self.obter_acesso_por_id(acesso_id)
        
        if not acesso:
            return False
        
        try:
            self.db.delete(acesso)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao deletar acesso")
