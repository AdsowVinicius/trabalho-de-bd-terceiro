import React, { useEffect, useState } from 'react'
import api from '../api'

export default function ControleAcesso(){
  const [aba, setAba] = useState('pessoal')
  const [acessosPessoais, setAcessosPessoais] = useState([])
  const [acessosVeiculares, setAcessosVeiculares] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    carregarAcessos()
    
    // Auto-refresh a cada 10 segundos
    const intervalo = setInterval(carregarAcessos, 10000)
    
    // Limpar intervalo quando sair da página
    return () => clearInterval(intervalo)
  }, [])

  async function carregarAcessos(){
    setLoading(true)
    const token = localStorage.getItem('token')
    try {
      // Carregar todos os acessos pessoais
      const resPessoal = await api.getAcessosPessoaisAtivos(token)
      if(resPessoal.data){
        // Filtrar apenas os que têm hora_saida vazio (ainda estão dentro)
        const ativos = resPessoal.data.filter(a => !a.hora_saida)
        setAcessosPessoais(ativos)
      }

      // Carregar todos os acessos veiculares
      const resVeicular = await api.getAcessosVeiculaesAtivos(token)
      if(resVeicular.data){
        // Filtrar apenas os que têm hora_saida vazio (ainda estão dentro)
        const ativos = resVeicular.data.filter(a => !a.hora_saida)
        setAcessosVeiculares(ativos)
      }
    } catch(err){
      console.error('Erro ao carregar acessos:', err)
    }
    setLoading(false)
  }

  async function darBaixaPessoal(acessoId){
    if(!window.confirm('Dar saída para este visitante?')) return

    const token = localStorage.getItem('token')
    try {
      console.log('Registrando saída pessoal ID:', acessoId)
      const res = await api.darSaidaPessoal(acessoId, token)
      console.log('Resposta saída pessoal:', res)
      if(res.status === 200){
        alert('Saída registrada com sucesso!')
        // Remover do estado imediatamente
        setAcessosPessoais(acessosPessoais.filter(a => a.id_acesso_pessoal !== acessoId))
      } else {
        alert('Erro: Status ' + res.status + ' - ' + JSON.stringify(res.data))
      }
    } catch(err){
      console.error('Erro completo:', err)
      alert('Erro ao registrar saída: ' + (err.message || JSON.stringify(err)))
    }
  }

  async function darBaixaVeicular(acessoId){
    if(!window.confirm('Dar saída para este veículo?')) return

    const token = localStorage.getItem('token')
    try {
      console.log('Registrando saída veicular ID:', acessoId)
      const res = await api.darSaidaVeicular(acessoId, token)
      console.log('Resposta saída veicular:', res)
      if(res.status === 200){
        alert('Saída registrada com sucesso!')
        // Remover do estado imediatamente
        setAcessosVeiculares(acessosVeiculares.filter(a => a.id_acesso_veiculo !== acessoId))
      } else {
        alert('Erro: Status ' + res.status + ' - ' + JSON.stringify(res.data))
      }
    } catch(err){
      console.error('Erro completo:', err)
      alert('Erro ao registrar saída: ' + (err.message || JSON.stringify(err)))
    }
  }

  const estilosAba = (ativo) => ({
    padding: '12px 20px',
    border: 'none',
    backgroundColor: ativo ? '#2196F3' : '#ddd',
    color: ativo ? '#fff' : '#333',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: 'bold',
    borderRadius: '4px 4px 0 0',
    marginRight: '5px'
  })

  const estiloTabela = {
    width: '100%',
    borderCollapse: 'collapse',
    marginTop: '20px'
  }

  const estiloLinha = {
    borderBottom: '1px solid #ddd',
    padding: '12px'
  }

  const estiloHeader = {
    backgroundColor: '#f5f5f5',
    fontWeight: 'bold',
    padding: '12px',
    textAlign: 'left',
    borderBottom: '2px solid #2196F3'
  }

  return (
    <div style={{ maxWidth: 1200, margin: '20px auto', padding: '20px' }}>
      <h2>Controle de Acesso</h2>

      {/* Abas */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <button
          onClick={() => setAba('pessoal')}
          style={estilosAba(aba === 'pessoal')}
        >
          Acessos Pessoais
        </button>
        <button
          onClick={() => setAba('veicular')}
          style={estilosAba(aba === 'veicular')}
        >
          Acessos Veiculares
        </button>
      </div>

      {/* Conteúdo */}
      <div style={{ border: '1px solid #ddd', borderRadius: '0 4px 4px 4px', padding: '20px', backgroundColor: '#fff' }}>
        {loading && <p>Carregando...</p>}

        {aba === 'pessoal' && (
          <div>
            <h3>Acessos Pessoais Ativos</h3>
            {acessosPessoais.length === 0 ? (
              <p style={{ color: '#666' }}>Nenhum acesso pessoal ativo no momento</p>
            ) : (
              <table style={estiloTabela}>
                <thead>
                  <tr>
                    <th style={estiloHeader}>ID</th>
                    <th style={estiloHeader}>Usuário ID</th>
                    <th style={estiloHeader}>Entrada</th>
                    <th style={estiloHeader}>Saída</th>
                    <th style={estiloHeader}>Motivo</th>
                    <th style={estiloHeader}>Observação</th>
                    <th style={estiloHeader}>Ação</th>
                  </tr>
                </thead>
                <tbody>
                  {acessosPessoais.map(acesso => (
                    <tr key={acesso.id_acesso_pessoal} style={estiloLinha}>
                      <td style={{ padding: '12px' }}>{acesso.id_acesso_pessoal}</td>
                      <td style={{ padding: '12px' }}>{acesso.id_usuario}</td>
                      <td style={{ padding: '12px' }}>
                        {acesso.hora_entrada ? new Date(acesso.hora_entrada).toLocaleString('pt-BR') : 'N/A'}
                      </td>
                      <td style={{ padding: '12px' }}>
                        {acesso.hora_saida ? new Date(acesso.hora_saida).toLocaleString('pt-BR') : '-'}
                      </td>
                      <td style={{ padding: '12px' }}>{acesso.motivo_visita || 'N/A'}</td>
                      <td style={{ padding: '12px' }}>{acesso.observacao || '-'}</td>
                      <td style={{ padding: '12px' }}>
                        {!acesso.hora_saida && (
                          <button
                            onClick={() => darBaixaPessoal(acesso.id_acesso_pessoal)}
                            style={{
                              padding: '8px 16px',
                              backgroundColor: '#f44336',
                              color: '#fff',
                              border: 'none',
                              borderRadius: '4px',
                              cursor: 'pointer',
                              fontSize: '12px'
                            }}
                          >
                            Saída
                          </button>
                        )}
                        {acesso.hora_saida && (
                          <span style={{ color: '#4CAF50', fontWeight: 'bold' }}>Saído</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}

        {aba === 'veicular' && (
          <div>
            <h3>Acessos Veiculares Ativos</h3>
            {acessosVeiculares.length === 0 ? (
              <p style={{ color: '#666' }}>Nenhum acesso veicular ativo no momento</p>
            ) : (
              <table style={estiloTabela}>
                <thead>
                  <tr>
                    <th style={estiloHeader}>ID</th>
                    <th style={estiloHeader}>Veículo ID</th>
                    <th style={estiloHeader}>Responsável ID</th>
                    <th style={estiloHeader}>Entrada</th>
                    <th style={estiloHeader}>Saída</th>
                    <th style={estiloHeader}>Tipo Serviço</th>
                    <th style={estiloHeader}>Observação</th>
                    <th style={estiloHeader}>Ação</th>
                  </tr>
                </thead>
                <tbody>
                  {acessosVeiculares.map(acesso => (
                    <tr key={acesso.id_acesso_veiculo} style={estiloLinha}>
                      <td style={{ padding: '12px' }}>{acesso.id_acesso_veiculo}</td>
                      <td style={{ padding: '12px' }}>{acesso.id_veiculo}</td>
                      <td style={{ padding: '12px' }}>{acesso.id_responsavel}</td>
                      <td style={{ padding: '12px' }}>
                        {acesso.hora_entrada ? new Date(acesso.hora_entrada).toLocaleString('pt-BR') : 'N/A'}
                      </td>
                      <td style={{ padding: '12px' }}>
                        {acesso.hora_saida ? new Date(acesso.hora_saida).toLocaleString('pt-BR') : '-'}
                      </td>
                      <td style={{ padding: '12px' }}>{acesso.id_tipo_servico || 'N/A'}</td>
                      <td style={{ padding: '12px' }}>{acesso.observacao || '-'}</td>
                      <td style={{ padding: '12px' }}>
                        {!acesso.hora_saida && (
                          <button
                            onClick={() => darBaixaVeicular(acesso.id_acesso_veiculo)}
                            style={{
                              padding: '8px 16px',
                              backgroundColor: '#f44336',
                              color: '#fff',
                              border: 'none',
                              borderRadius: '4px',
                              cursor: 'pointer',
                              fontSize: '12px'
                            }}
                          >
                            Saída
                          </button>
                        )}
                        {acesso.hora_saida && (
                          <span style={{ color: '#4CAF50', fontWeight: 'bold' }}>Saído</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>

      {/* Botão para recarregar */}
      <button
        onClick={carregarAcessos}
        style={{
          marginTop: '20px',
          padding: '10px 20px',
          backgroundColor: '#4CAF50',
          color: '#fff',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer'
        }}
      >
        Recarregar
      </button>
    </div>
  )
}
