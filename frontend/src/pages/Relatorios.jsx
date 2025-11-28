import React, { useEffect, useState } from 'react'
import api from '../api'
import '../styles.css'

export default function Relatorios() {
  const [abaSelecionada, setAbaSelecionada] = useState('visitantes-ativos')
  const [dados, setDados] = useState([])
  const [dadosFiltrados, setDadosFiltrados] = useState([])
  const [loading, setLoading] = useState(false)
  const [erro, setErro] = useState(null)
  const [pesquisa, setPesquisa] = useState('')
  const token = localStorage.getItem('token')

  // Função para carregar dados
  const carregarDados = async (endpoint) => {
    setLoading(true)
    setErro(null)
    setPesquisa('')
    try {
      const response = await fetch(`http://localhost:8001/relatorios/${endpoint}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      
      if (!response.ok) throw new Error('Erro ao carregar dados')
      
      const result = await response.json()
      setDados(result.dados || [])
      setDadosFiltrados(result.dados || [])
    } catch (err) {
      setErro(err.message)
      setDados([])
      setDadosFiltrados([])
    } finally {
      setLoading(false)
    }
  }

  // Função para filtrar dados na pesquisa
  const handlePesquisa = (valor) => {
    setPesquisa(valor)
    
    if (!valor.trim()) {
      setDadosFiltrados(dados)
      return
    }

    const termoLower = valor.toLowerCase()
    const filtrados = dados.filter(linha => 
      Object.values(linha).some(valor => 
        String(valor).toLowerCase().includes(termoLower)
      )
    )
    setDadosFiltrados(filtrados)
  }

  // Carregar dados quando mudar a aba
  useEffect(() => {
    carregarDados(abaSelecionada)
  }, [abaSelecionada])

  // Função para exportar como CSV
  const exportarCSV = () => {
    if (dadosFiltrados.length === 0) return

    const headers = Object.keys(dadosFiltrados[0])
    const csv = [
      headers.join(','),
      ...dadosFiltrados.map(row => 
        headers.map(header => {
          const valor = row[header]
          // Escapar aspas e vírgulas
          if (typeof valor === 'string' && (valor.includes(',') || valor.includes('"'))) {
            return `"${valor.replace(/"/g, '""')}"`
          }
          return valor
        }).join(',')
      )
    ].join('\n')

    const blob = new Blob([csv], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `relatorio-${abaSelecionada}-${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    window.URL.revokeObjectURL(url)
  }

  return (
    <div className="relatorios-container">
      <h1>📊 Relatórios e Consultas</h1>
      
      {/* Abas */}
      <div className="relatorios-abas">
        <button 
          className={`aba-btn ${abaSelecionada === 'visitantes-ativos' ? 'ativa' : ''}`}
          onClick={() => setAbaSelecionada('visitantes-ativos')}
        >
          👥 Visitantes Ativos
        </button>
        <button 
          className={`aba-btn ${abaSelecionada === 'veiculos-ativos' ? 'ativa' : ''}`}
          onClick={() => setAbaSelecionada('veiculos-ativos')}
        >
          🚗 Veículos Ativos
        </button>
        <button 
          className={`aba-btn ${abaSelecionada === 'acessos-pessoais-detalhado' ? 'ativa' : ''}`}
          onClick={() => setAbaSelecionada('acessos-pessoais-detalhado')}
        >
          📋 Histórico Pessoal
        </button>
        <button 
          className={`aba-btn ${abaSelecionada === 'acessos-veiculares-detalhado' ? 'ativa' : ''}`}
          onClick={() => setAbaSelecionada('acessos-veiculares-detalhado')}
        >
          📦 Histórico Veicular
        </button>
      </div>

      {/* Controles */}
      <div className="relatorios-controles">
        <button onClick={() => carregarDados(abaSelecionada)} className="btn-recarregar">
          🔄 Recarregar
        </button>
        <button onClick={exportarCSV} className="btn-exportar" disabled={dadosFiltrados.length === 0}>
          📥 Exportar CSV
        </button>
      </div>

      {/* Caixa de Pesquisa */}
      {dados.length > 0 && (
        <div className="relatorios-pesquisa">
          <input 
            type="text"
            placeholder="🔍 Pesquisar em todos os campos..."
            value={pesquisa}
            onChange={(e) => handlePesquisa(e.target.value)}
            className="relatorios-input-pesquisa"
          />
          <span className="relatorios-info-pesquisa">
            {dadosFiltrados.length} de {dados.length} registros
          </span>
        </div>
      )}

      {/* Conteúdo */}
      <div className="relatorios-conteudo">
        {loading && <div className="relatorios-loading">⏳ Carregando...</div>}
        
        {erro && <div className="relatorios-erro">❌ {erro}</div>}
        
        {!loading && dados.length === 0 && !erro && (
          <div className="relatorios-vazio">📭 Nenhum dado para exibir</div>
        )}
        
        {!loading && dadosFiltrados.length === 0 && dados.length > 0 && (
          <div className="relatorios-vazio">🔍 Nenhum resultado encontrado para "{pesquisa}"</div>
        )}
        
        {!loading && dadosFiltrados.length > 0 && (
          <div className="relatorios-tabela-wrapper">
            <table className="relatorios-tabela">
              <thead>
                <tr>
                  {Object.keys(dadosFiltrados[0]).map(coluna => (
                    <th key={coluna}>{coluna.replace(/_/g, ' ').toUpperCase()}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {dadosFiltrados.map((linha, idx) => (
                  <tr key={idx}>
                    {Object.values(linha).map((valor, idx2) => (
                      <td key={idx2}>
                        {typeof valor === 'string' && valor.length > 50 
                          ? valor.substring(0, 50) + '...' 
                          : String(valor)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Resumo */}
      {!loading && dadosFiltrados.length > 0 && (
        <div className="relatorios-resumo">
          Total exibido: <strong>{dadosFiltrados.length}</strong> {dadosFiltrados.length === dados.length ? `de ${dados.length}` : `(filtrado de ${dados.length})`}
        </div>
      )}
    </div>
  )
}
