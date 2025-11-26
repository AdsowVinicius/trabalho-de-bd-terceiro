from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from ..models.veiculo import Veiculo
from ..schemas.veiculo_schema import VeiculoCreate, VeiculoUpdate


class VeiculoService:
    """Serviço de negócio para operações de veículos"""
    
    def __init__(self, db: Session):
        """
        Inicializa o serviço de veículos
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db
    
    def criar_veiculo(self, veiculo_data: VeiculoCreate) -> Veiculo:
        """
        Cria um novo veículo
        
        Args:
            veiculo_data: Dados do veículo a ser criado
            
        Returns:
            Veículo criado
            
        Raises:
            ValueError: Se a placa já existe
        """
        # Verificar se placa já existe
        veiculo_existente = self.db.query(Veiculo).filter(
            Veiculo.placa == veiculo_data.placa
        ).first()
        
        if veiculo_existente:
            raise ValueError("Placa já cadastrada")
        
        novo_veiculo = Veiculo(
            placa=veiculo_data.placa,
            modelo=veiculo_data.modelo,
            ano=veiculo_data.ano,
            id_responsavel=veiculo_data.id_responsavel
        )
        
        try:
            self.db.add(novo_veiculo)
            self.db.commit()
            self.db.refresh(novo_veiculo)
            return novo_veiculo
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao criar veículo")
    
    def obter_veiculo_por_id(self, veiculo_id: int) -> Optional[Veiculo]:
        """
        Obtém um veículo pelo ID
        
        Args:
            veiculo_id: ID do veículo
            
        Returns:
            Veículo encontrado ou None
        """
        return self.db.query(Veiculo).filter(Veiculo.id_veiculo == veiculo_id).first()
    
    def obter_veiculo_por_placa(self, placa: str) -> Optional[Veiculo]:
        """
        Obtém um veículo pela placa
        
        Args:
            placa: Placa do veículo
            
        Returns:
            Veículo encontrado ou None
        """
        return self.db.query(Veiculo).filter(Veiculo.placa == placa).first()
    
    def listar_veiculos(self, skip: int = 0, limit: int = 10) -> List[Veiculo]:
        """
        Lista todos os veículos com paginação
        
        Args:
            skip: Número de registros a pular
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de veículos
        """
        return self.db.query(Veiculo).offset(skip).limit(limit).all()
    
    def listar_veiculos_por_responsavel(self, responsavel_id: int) -> List[Veiculo]:
        """
        Lista veículos de um responsável
        
        Args:
            responsavel_id: ID do responsável
            
        Returns:
            Lista de veículos
        """
        return self.db.query(Veiculo).filter(
            Veiculo.id_responsavel == responsavel_id
        ).all()
    
    def atualizar_veiculo(self, veiculo_id: int, veiculo_data: VeiculoUpdate) -> Optional[Veiculo]:
        """
        Atualiza um veículo existente
        
        Args:
            veiculo_id: ID do veículo
            veiculo_data: Dados a serem atualizados
            
        Returns:
            Veículo atualizado ou None se não encontrado
        """
        veiculo = self.obter_veiculo_por_id(veiculo_id)
        
        if not veiculo:
            return None
        
        # Atualizar apenas os campos fornecidos
        if veiculo_data.modelo is not None:
            veiculo.modelo = veiculo_data.modelo
        if veiculo_data.ano is not None:
            veiculo.ano = veiculo_data.ano
        if veiculo_data.id_responsavel is not None:
            veiculo.id_responsavel = veiculo_data.id_responsavel
        
        try:
            self.db.commit()
            self.db.refresh(veiculo)
            return veiculo
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao atualizar veículo")
    
    def deletar_veiculo(self, veiculo_id: int) -> bool:
        """
        Deleta um veículo
        
        Args:
            veiculo_id: ID do veículo
            
        Returns:
            True se deletado, False se não encontrado
        """
        veiculo = self.obter_veiculo_por_id(veiculo_id)
        
        if not veiculo:
            return False
        
        try:
            self.db.delete(veiculo)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao deletar veículo - pode ter acessos relacionados")
