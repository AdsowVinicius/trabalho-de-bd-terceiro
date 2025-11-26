from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from ..models.acesso_veicular import AcessoVeicular
from ..schemas.acesso_veicular_schema import AcessoVeicularCreate, AcessoVeicularUpdate
from datetime import datetime


class AcessoVeicularService:
    """Serviço de negócio para operações de acessos veiculares"""
    
    def __init__(self, db: Session):
        """
        Inicializa o serviço de acessos veiculares
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db
    
    def criar_acesso(self, acesso_data: AcessoVeicularCreate) -> AcessoVeicular:
        """
        Registra uma entrada veicular
        
        Args:
            acesso_data: Dados do acesso a ser criado
            
        Returns:
            Acesso veicular criado
        """
        novo_acesso = AcessoVeicular(
            id_veiculo=acesso_data.id_veiculo,
            id_responsavel=acesso_data.id_responsavel,
            id_tipo_servico=acesso_data.id_tipo_servico,
            id_transportadora=acesso_data.id_transportadora,
            nota_fiscal_entrada=acesso_data.nota_fiscal_entrada,
            nota_fiscal_saida=acesso_data.nota_fiscal_saida,
            observacao=acesso_data.observacao
        )
        
        try:
            self.db.add(novo_acesso)
            self.db.commit()
            self.db.refresh(novo_acesso)
            return novo_acesso
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao registrar acesso veicular")
    
    def obter_acesso_por_id(self, acesso_id: int) -> Optional[AcessoVeicular]:
        """
        Obtém um acesso pelo ID
        
        Args:
            acesso_id: ID do acesso
            
        Returns:
            Acesso encontrado ou None
        """
        return self.db.query(AcessoVeicular).filter(
            AcessoVeicular.id_acesso_veiculo == acesso_id
        ).first()
    
    def listar_acessos(self, skip: int = 0, limit: int = 10) -> List[AcessoVeicular]:
        """
        Lista todos os acessos com paginação
        
        Args:
            skip: Número de registros a pular
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de acessos
        """
        return self.db.query(AcessoVeicular).offset(skip).limit(limit).all()
    
    def listar_acessos_por_veiculo(self, veiculo_id: int) -> List[AcessoVeicular]:
        """
        Lista acessos de um veículo
        
        Args:
            veiculo_id: ID do veículo
            
        Returns:
            Lista de acessos
        """
        return self.db.query(AcessoVeicular).filter(
            AcessoVeicular.id_veiculo == veiculo_id
        ).all()
    
    def listar_acessos_por_responsavel(self, responsavel_id: int) -> List[AcessoVeicular]:
        """
        Lista acessos de um responsável
        
        Args:
            responsavel_id: ID do responsável
            
        Returns:
            Lista de acessos
        """
        return self.db.query(AcessoVeicular).filter(
            AcessoVeicular.id_responsavel == responsavel_id
        ).all()
    
    def listar_veiculos_ativos(self) -> List[AcessoVeicular]:
        """
        Lista veículos atualmente dentro (sem hora_saida)
        
        Returns:
            Lista de acessos ativos
        """
        return self.db.query(AcessoVeicular).filter(
            AcessoVeicular.hora_saida.is_(None)
        ).all()
    
    def registrar_saida(self, acesso_id: int, acesso_data: AcessoVeicularUpdate) -> Optional[AcessoVeicular]:
        """
        Registra a saída de um veículo
        
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
        
        if acesso_data.nota_fiscal_saida is not None:
            acesso.nota_fiscal_saida = acesso_data.nota_fiscal_saida
        
        if acesso_data.observacao is not None:
            acesso.observacao = acesso_data.observacao
        
        try:
            self.db.commit()
            self.db.refresh(acesso)
            return acesso
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao registrar saída")
    
    def atualizar_acesso(self, acesso_id: int, acesso_data: AcessoVeicularUpdate) -> Optional[AcessoVeicular]:
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
        
        if acesso_data.hora_saida is not None:
            acesso.hora_saida = acesso_data.hora_saida
        if acesso_data.nota_fiscal_saida is not None:
            acesso.nota_fiscal_saida = acesso_data.nota_fiscal_saida
        if acesso_data.observacao is not None:
            acesso.observacao = acesso_data.observacao
        
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
