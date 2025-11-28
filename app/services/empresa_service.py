from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from ..models.empresa import Empresa
from ..schemas.empresa_schema import EmpresaCreate, EmpresaUpdate


class EmpresaService:
    """Serviço de negócio para operações de empresas"""
    
    def __init__(self, db: Session):
        """
        Inicializa o serviço de empresas
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db
    
    def criar_empresa(self, empresa_data: EmpresaCreate) -> Empresa:
        """
        Cria uma nova empresa
        
        Args:
            empresa_data: Dados da empresa a ser criada
            
        Returns:
            Empresa criada
            
        Raises:
            ValueError: Se o CNPJ já existe
        """
        # Verificar se CNPJ já existe
        empresa_existente = self.db.query(Empresa).filter(
            Empresa.cnpj == empresa_data.cnpj
        ).first()
        
        if empresa_existente:
            raise ValueError("CNPJ já cadastrado")
        
        nova_empresa = Empresa(
            nome_empresa=empresa_data.nome_empresa,
            cnpj=empresa_data.cnpj,
            id_tipo_empresa=empresa_data.id_tipo_empresa,
            responsavel=empresa_data.responsavel,
            contato=empresa_data.contato
        )
        
        try:
            self.db.add(nova_empresa)
            self.db.commit()
            self.db.refresh(nova_empresa)
            return nova_empresa
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao criar empresa - pode existir duplicação")
    
    def obter_empresa_por_id(self, id_empresa: int) -> Optional[Empresa]:
        """
        Obtém uma empresa pelo ID
        
        Args:
            id_empresa: ID da empresa
            
        Returns:
            Empresa encontrada ou None
        """
        return self.db.query(Empresa).filter(Empresa.id_empresa == id_empresa).first()
    
    def obter_empresa_por_cnpj(self, cnpj: str) -> Optional[Empresa]:
        """
        Obtém uma empresa pelo CNPJ
        
        Args:
            cnpj: CNPJ da empresa
            
        Returns:
            Empresa encontrada ou None
        """
        return self.db.query(Empresa).filter(Empresa.cnpj == cnpj).first()
    
    def listar_empresas(self) -> List[Empresa]:
        """
        Lista todas as empresas
        
        Returns:
            Lista de empresas
        """
        return self.db.query(Empresa).order_by(Empresa.nome_empresa).all()
    
    def atualizar_empresa(self, id_empresa: int, empresa_data: EmpresaUpdate) -> Optional[Empresa]:
        """
        Atualiza uma empresa
        
        Args:
            id_empresa: ID da empresa
            empresa_data: Dados para atualizar
            
        Returns:
            Empresa atualizada ou None
            
        Raises:
            ValueError: Se o CNPJ já existe em outra empresa
        """
        empresa = self.db.query(Empresa).filter(Empresa.id_empresa == id_empresa).first()
        
        if not empresa:
            return None
        
        # Verificar se novo CNPJ já existe em outra empresa
        if empresa.cnpj != empresa_data.cnpj:
            cnpj_existente = self.db.query(Empresa).filter(
                Empresa.cnpj == empresa_data.cnpj
            ).first()
            if cnpj_existente:
                raise ValueError("CNPJ já cadastrado em outra empresa")
        
        try:
            empresa.nome_empresa = empresa_data.nome_empresa
            empresa.cnpj = empresa_data.cnpj
            empresa.id_tipo_empresa = empresa_data.id_tipo_empresa
            empresa.responsavel = empresa_data.responsavel
            empresa.contato = empresa_data.contato
            
            self.db.commit()
            self.db.refresh(empresa)
            return empresa
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao atualizar empresa")
    
    def deletar_empresa(self, id_empresa: int) -> bool:
        """
        Deleta uma empresa
        
        Args:
            id_empresa: ID da empresa
            
        Returns:
            True se deletada com sucesso, False caso contrário
            
        Raises:
            ValueError: Se houver acessos relacionados
        """
        empresa = self.db.query(Empresa).filter(Empresa.id_empresa == id_empresa).first()
        
        if not empresa:
            return False
        
        try:
            self.db.delete(empresa)
            self.db.commit()
            return True
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError("Erro ao deletar empresa - pode ter acessos relacionados")

