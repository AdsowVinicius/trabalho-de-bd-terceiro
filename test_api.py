"""
Script de teste para a API de Controle de Acesso
Testa os endpoints básicos da aplicação
"""

import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8001"

class APITester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.token = None
        self.usuario_id = None
        self.veiculo_id = None
        self.acesso_pessoal_id = None
        self.acesso_veicular_id = None
        self.db_connected = False
    
    def verificar_conexao(self) -> bool:
        """Verifica se o servidor está rodando e o banco está conectado"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Servidor FastAPI está rodando")
                return True
        except requests.exceptions.ConnectionError:
            print("❌ ERRO: Não foi possível conectar ao servidor")
            print("   Certifique-se de que o servidor está rodando: python run.py")
            return False
        except Exception as e:
            print(f"❌ ERRO ao conectar: {str(e)}")
            return False
    
    def _print_response(self, method: str, url: str, status_code: int, data: dict):
        """Imprime informações da resposta"""
        print(f"\n{'='*60}")
        print(f"[{method}] {url}")
        print(f"Status: {status_code}")
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        print(f"{'='*60}")
    
    def test_health(self):
        """Testa o health check"""
        print("\n✓ Testando Health Check...")
        response = requests.get(f"{self.base_url}/health")
        self._print_response("GET", "/health", response.status_code, response.json())
        return response.status_code == 200
    
    def test_registrar_usuario(self):
        """Testa registro de novo usuário"""
        print("\n✓ Testando Registro de Usuário...")
        payload = {
            "nome": "João Silva",
            "documento": "12345678900",
            "id_tipo_usuario": 1,
            "login": "joao_silva",
            "senha": "senha123",
            "id_perfil_acesso": 1,
            "contato": "11999999999"
        }
        try:
            response = requests.post(f"{self.base_url}/usuarios/registro", json=payload)
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"\n{'='*60}")
            print(f"[POST] /usuarios/registro")
            print(f"Status: {response.status_code}")
            print(f"Erro: Servidor retornou resposta inválida")
            print(f"Mensagem: {response.text[:200] if response.text else 'Sem conteúdo'}")
            print("⚠️  POSSÍVEL CAUSA: Banco de dados não está conectado")
            print(f"{'='*60}")
            return False
        
        self._print_response("POST", "/usuarios/registro", response.status_code, data)
        
        if response.status_code == 201:
            data = response.json()
            self.usuario_id = data.get("id_usuario")
            return True
        return False
    
    def test_login(self):
        """Testa login e obtenção de token"""
        print("\n✓ Testando Login...")
        payload = {
            "login": "joao_silva",
            "senha": "senha123"
        }
        response = requests.post(f"{self.base_url}/usuarios/login", json=payload)
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("❌ Erro ao decodificar resposta JSON - Banco de dados pode não estar disponível")
            return False
        self._print_response("POST", "/usuarios/login", response.status_code, response_data)
        
        if response.status_code == 200:
            self.token = response_data.get("access_token")
            return True
        return False
    
    def test_obter_usuario(self):
        """Testa obtenção de dados do usuário"""
        if not self.usuario_id:
            print("⚠ Pulando teste: usuário não registrado")
            return False
        
        print("\n✓ Testando Obter Usuário...")
        response = requests.get(f"{self.base_url}/usuarios/{self.usuario_id}")
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("❌ Erro ao decodificar resposta JSON - Banco de dados pode não estar disponível")
            return False
        self._print_response("GET", f"/usuarios/{self.usuario_id}", response.status_code, response_data)
        return response.status_code == 200
    
    def test_criar_veiculo(self):
        """Testa criação de veículo"""
        if not self.usuario_id:
            print("⚠ Pulando teste: usuário não registrado")
            return False
        
        print("\n✓ Testando Criar Veículo...")
        payload = {
            "placa": "ABC-1234",
            "modelo": "Fiat Uno",
            "ano": 2020,
            "id_responsavel": self.usuario_id
        }
        response = requests.post(f"{self.base_url}/veiculos/", json=payload)
        self._print_response("POST", "/veiculos/", response.status_code, response.json())
        
        if response.status_code == 201:
            data = response.json()
            self.veiculo_id = data.get("id_veiculo")
            return True
        return False
    
    def test_obter_veiculo(self):
        """Testa obtenção de dados do veículo"""
        if not self.veiculo_id:
            print("⚠ Pulando teste: veículo não criado")
            return False
        
        print("\n✓ Testando Obter Veículo...")
        response = requests.get(f"{self.base_url}/veiculos/{self.veiculo_id}")
        self._print_response("GET", f"/veiculos/{self.veiculo_id}", response.status_code, response.json())
        return response.status_code == 200
    
    def test_registrar_acesso_pessoal(self):
        """Testa registro de acesso pessoal"""
        if not self.usuario_id:
            print("⚠ Pulando teste: usuário não registrado")
            return False
        
        print("\n✓ Testando Registrar Acesso Pessoal...")
        payload = {
            "id_usuario": self.usuario_id,
            "id_tipo_acesso": 1,
            "id_empresa_visitada": 1,
            "motivo_visita": "Reunião de trabalho"
        }
        response = requests.post(f"{self.base_url}/acessos-pessoais/", json=payload)
        self._print_response("POST", "/acessos-pessoais/", response.status_code, response.json())
        
        if response.status_code == 201:
            data = response.json()
            self.acesso_pessoal_id = data.get("id_acesso_pessoal")
            return True
        return False
    
    def test_registrar_saida_pessoal(self):
        """Testa registro de saída pessoal"""
        if not self.acesso_pessoal_id:
            print("⚠ Pulando teste: acesso pessoal não registrado")
            return False
        
        print("\n✓ Testando Registrar Saída Pessoal...")
        payload = {
            "observacao": "Saída sem ocorrências"
        }
        response = requests.put(
            f"{self.base_url}/acessos-pessoais/{self.acesso_pessoal_id}/saida",
            json=payload
        )
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("❌ Erro ao decodificar resposta JSON - Banco de dados pode não estar disponível")
            return False
        self._print_response("PUT", f"/acessos-pessoais/{self.acesso_pessoal_id}/saida", 
                           response.status_code, response_data)
        return response.status_code == 200
    
    def test_registrar_acesso_veicular(self):
        """Testa registro de acesso veicular"""
        if not self.veiculo_id or not self.usuario_id:
            print("⚠ Pulando teste: veículo ou usuário não criado")
            return False
        
        print("\n✓ Testando Registrar Acesso Veicular...")
        payload = {
            "id_veiculo": self.veiculo_id,
            "id_responsavel": self.usuario_id,
            "id_tipo_servico": 1,
            "nota_fiscal_entrada": "NF-123456"
        }
        response = requests.post(f"{self.base_url}/acessos-veiculares/", json=payload)
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("❌ Erro ao decodificar resposta JSON - Banco de dados pode não estar disponível")
            return False
        self._print_response("POST", "/acessos-veiculares/", response.status_code, response_data)
        
        if response.status_code == 201:
            self.acesso_veicular_id = response_data.get("id_acesso_veiculo")
            return True
        return False
    
    def test_registrar_saida_veicular(self):
        """Testa registro de saída veicular"""
        if not self.acesso_veicular_id:
            print("⚠ Pulando teste: acesso veicular não registrado")
            return False
        
        print("\n✓ Testando Registrar Saída Veicular...")
        payload = {
            "nota_fiscal_saida": "NF-123457",
            "observacao": "Coleta realizada com sucesso"
        }
        response = requests.put(
            f"{self.base_url}/acessos-veiculares/{self.acesso_veicular_id}/saida",
            json=payload
        )
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("❌ Erro ao decodificar resposta JSON - Banco de dados pode não estar disponível")
            return False
        self._print_response("PUT", f"/acessos-veiculares/{self.acesso_veicular_id}/saida",
                           response.status_code, response_data)
        return response.status_code == 200
    
    def test_listar_visitantes_ativos(self):
        """Testa listagem de visitantes ativos"""
        print("\n✓ Testando Listar Visitantes Ativos...")
        response = requests.get(f"{self.base_url}/acessos-pessoais/ativos/visitantes")
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("❌ Erro ao decodificar resposta JSON - Banco de dados pode não estar disponível")
            return False
        self._print_response("GET", "/acessos-pessoais/ativos/visitantes", 
                           response.status_code, response_data)
        return response.status_code == 200
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("\n" + "="*60)
        print("INICIANDO TESTES DA API DE CONTROLE DE ACESSO")
        print("="*60)
        
        # Verificar conexão com servidor
        if not self.verificar_conexao():
            print("\n" + "="*60)
            print("⚠️  TESTES CANCELADOS - SERVIDOR INDISPONÍVEL")
            print("="*60)
            return
        
        # Verificar conexão com banco de dados
        print("✅ Testando conexão com banco de dados...")
        if not self.test_health():
            print("❌ Servidor respondeu mas pode haver problemas")
        
        print("\n" + "="*60)
        print("COMEÇANDO TESTES DOS ENDPOINTS")
        print("="*60)
        
        results = {
            "Health Check": self.test_health(),
            "Registrar Usuário": self.test_registrar_usuario(),
            "Login": self.test_login(),
            "Obter Usuário": self.test_obter_usuario(),
            "Criar Veículo": self.test_criar_veiculo(),
            "Obter Veículo": self.test_obter_veiculo(),
            "Registrar Acesso Pessoal": self.test_registrar_acesso_pessoal(),
            "Registrar Saída Pessoal": self.test_registrar_saida_pessoal(),
            "Registrar Acesso Veicular": self.test_registrar_acesso_veicular(),
            "Registrar Saída Veicular": self.test_registrar_saida_veicular(),
            "Listar Visitantes Ativos": self.test_listar_visitantes_ativos(),
        }
        
        # Resumo dos testes
        print("\n" + "="*60)
        print("RESUMO DOS TESTES")
        print("="*60)
        
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✓ PASSOU" if result else "✗ FALHOU"
            print(f"{test_name}: {status}")
        
        print(f"\nTotal: {passed}/{total} testes passaram")
        print("="*60)


if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()
