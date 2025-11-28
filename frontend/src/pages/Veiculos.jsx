import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'
import FormField from '../components/FormField'

export default function Veiculos(){
  const [veiculos, setVeiculos] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [editando, setEditando] = useState(null)
  const [responsaveis, setResponsaveis] = useState([])
  const [form, setForm] = useState({
    placa: '',
    modelo: '',
    ano: new Date().getFullYear(),
    id_responsavel: ''
  })
  const [searchPlaca, setSearchPlaca] = useState('')
  const [searchResponsavel, setSearchResponsavel] = useState('')
  const [responsaveisFiltrados, setResponsaveisFiltrados] = useState([])
  const [showResponsaveisList, setShowResponsaveisList] = useState(false)
  const [responsavelSelecionado, setResponsavelSelecionado] = useState(null)
  const token = localStorage.getItem('token')
  const nav = useNavigate()

  // Carregar dados
  useEffect(() => {
    carregarVeiculos()
    carregarResponsaveis()
  }, [])

  async function carregarVeiculos() {
    try {
      const resp = await fetch('http://127.0.0.1:8001/veiculos/', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (resp.ok) {
        const data = await resp.json()
        setVeiculos(data)
      }
    } catch (e) {
      console.error('Erro ao carregar veículos:', e)
    }
  }

  async function carregarResponsaveis() {
    try {
      const r = await fetch('http://127.0.0.1:8001/lookups/responsaveis')
      if (r.ok) {
        const data = await r.json()
        setResponsaveis(data)
      }
    } catch (e) {
      console.error('Erro ao carregar responsáveis:', e)
    }
  }

  // Busca responsaveis
  const handleSearchResponsavel = (valor) => {
    setSearchResponsavel(valor)
    if (valor.trim()) {
      const filtrados = responsaveis.filter(r =>
        r.nome.toLowerCase().includes(valor.toLowerCase()) ||
        r.documento.includes(valor) ||
        r.login.toLowerCase().includes(valor.toLowerCase())
      )
      setResponsaveisFiltrados(filtrados)
      setShowResponsaveisList(true)
    } else {
      setResponsaveisFiltrados([])
      setShowResponsaveisList(false)
    }
  }

  // Seleciona responsavel
  const selecionarResponsavel = (responsavel) => {
    setResponsavelSelecionado(responsavel)
    setForm({ ...form, id_responsavel: responsavel.id })
    setSearchResponsavel(`${responsavel.nome} (${responsavel.documento})`)
    setShowResponsaveisList(false)
  }

  // Novo veiculo
  function novoVeiculo() {
    setEditando(null)
    setForm({
      placa: '',
      modelo: '',
      ano: new Date().getFullYear(),
      id_responsavel: ''
    })
    setResponsavelSelecionado(null)
    setSearchResponsavel('')
    setShowForm(true)
  }

  // Editar veiculo
  function editarVeiculo(veiculo) {
    setEditando(veiculo.id_veiculo)
    const resp = responsaveis.find(r => r.id === veiculo.id_responsavel)
    if (resp) {
      setResponsavelSelecionado(resp)
      setSearchResponsavel(`${resp.nome} (${resp.documento})`)
    }
    setForm({
      placa: veiculo.placa,
      modelo: veiculo.modelo || '',
      ano: veiculo.ano || new Date().getFullYear(),
      id_responsavel: veiculo.id_responsavel
    })
    setShowForm(true)
  }

  // Salvar (criar ou atualizar)
  async function salvar(e) {
    e.preventDefault()
    
    if (!form.placa.trim()) {
      alert('Placa eh obrigatoria')
      return
    }
    if (!responsavelSelecionado) {
      alert('Selecione um responsavel')
      return
    }

    try {
      if (editando) {
        // Atualizar
        const resp = await fetch(`http://127.0.0.1:8001/veiculos/${editando}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            placa: form.placa,
            modelo: form.modelo,
            ano: parseInt(form.ano),
            id_responsavel: form.id_responsavel
          })
        })
        if (resp.ok) {
          alert('Veiculo atualizado com sucesso')
          carregarVeiculos()
          setShowForm(false)
        } else {
          const err = await resp.json()
          alert('Erro: ' + (err.detail || 'Erro ao atualizar'))
        }
      } else {
        // Criar
        const resp = await fetch('http://127.0.0.1:8001/veiculos/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            placa: form.placa,
            modelo: form.modelo,
            ano: parseInt(form.ano),
            id_responsavel: form.id_responsavel
          })
        })
        if (resp.ok) {
          alert('Veiculo criado com sucesso')
          carregarVeiculos()
          setShowForm(false)
          setForm({
            placa: '',
            modelo: '',
            ano: new Date().getFullYear(),
            id_responsavel: ''
          })
          setResponsavelSelecionado(null)
          setSearchResponsavel('')
        } else {
          const err = await resp.json()
          alert('Erro: ' + (err.detail || 'Erro ao criar'))
        }
      }
    } catch (e) {
      alert('Erro: ' + e.message)
    }
  }

  // Deletar
  async function deletar(id) {
    if (!window.confirm('Tem certeza que deseja deletar este veiculo?')) return
    
    try {
      const resp = await fetch(`http://127.0.0.1:8001/veiculos/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (resp.ok) {
        alert('Veiculo deletado com sucesso')
        carregarVeiculos()
      } else {
        const err = await resp.json()
        alert('Erro: ' + (err.detail || 'Erro ao deletar'))
      }
    } catch (e) {
      alert('Erro: ' + e.message)
    }
  }

  // Cancelar
  function cancelar() {
    setShowForm(false)
    setEditando(null)
    setForm({
      placa: '',
      modelo: '',
      ano: new Date().getFullYear(),
      id_responsavel: ''
    })
    setResponsavelSelecionado(null)
    setSearchResponsavel('')
  }

  // Filtrar veiculos
  const veiculosFiltrados = veiculos.filter(v =>
    v.placa.toLowerCase().includes(searchPlaca.toLowerCase())
  )

  return (
    <div style={{ maxWidth: 1200, margin: '20px auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Gestao de Veiculos</h2>
        <button onClick={novoVeiculo} style={{ backgroundColor: '#4CAF50', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Novo Veiculo
        </button>
      </div>

      {/* Formulario */}
      {showForm && (
        <div style={{ border: '2px solid #2196F3', padding: '20px', borderRadius: '8px', marginBottom: '20px', backgroundColor: '#f9f9f9' }}>
          <h3>{editando ? 'Editar Veiculo' : 'Novo Veiculo'}</h3>
          <form onSubmit={salvar}>
            <FormField label="Placa">
              <input
                type="text"
                required
                value={form.placa}
                onChange={e => setForm({ ...form, placa: e.target.value.toUpperCase() })}
                placeholder="Ex: ABC-1234"
                maxLength="10"
              />
            </FormField>

            <FormField label="Modelo">
              <input
                type="text"
                value={form.modelo}
                onChange={e => setForm({ ...form, modelo: e.target.value })}
                placeholder="Ex: Fiat Uno, Toyota Hilux"
              />
            </FormField>

            <FormField label="Ano">
              <input
                type="number"
                value={form.ano}
                onChange={e => setForm({ ...form, ano: parseInt(e.target.value) })}
                min="1980"
                max={new Date().getFullYear() + 1}
              />
            </FormField>

            <FormField label="Pesquisar Responsavel">
              <div style={{ position: 'relative' }}>
                <input
                  type="text"
                  required
                  placeholder="Digite nome, documento ou login"
                  value={searchResponsavel}
                  onChange={e => handleSearchResponsavel(e.target.value)}
                  onFocus={() => searchResponsavel.trim() && setShowResponsaveisList(true)}
                />
                {showResponsaveisList && (
                  <div style={{
                    position: 'absolute',
                    top: '100%',
                    left: 0,
                    right: 0,
                    border: '1px solid #ddd',
                    maxHeight: '200px',
                    overflowY: 'auto',
                    backgroundColor: 'white',
                    zIndex: 10
                  }}>
                    {responsaveisFiltrados.length > 0 ? (
                      responsaveisFiltrados.map(r =>
                        <div
                          key={r.id}
                          onClick={() => selecionarResponsavel(r)}
                          style={{
                            padding: '8px',
                            borderBottom: '1px solid #eee',
                            cursor: 'pointer',
                            backgroundColor: responsavelSelecionado?.id === r.id ? '#e3f2fd' : 'white'
                          }}
                        >
                          <strong>{r.nome}</strong> ({r.documento}) - {r.login}
                        </div>
                      )
                    ) : (
                      <div style={{ padding: '8px', color: '#999' }}>Nenhum responsavel encontrado</div>
                    )}
                  </div>
                )}
              </div>
              {responsavelSelecionado && (
                <button
                  type="button"
                  onClick={() => { setResponsavelSelecionado(null); setSearchResponsavel(''); setForm({ ...form, id_responsavel: '' }) }}
                  style={{ marginTop: '8px' }}
                >
                  Limpar Selecao
                </button>
              )}
            </FormField>

            <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
              <button type="submit" style={{ flex: 1, backgroundColor: '#4CAF50', color: 'white', padding: '10px' }}>
                {editando ? 'Atualizar' : 'Criar'} Veiculo
              </button>
              <button type="button" onClick={cancelar} style={{ flex: 1, backgroundColor: '#f44336', color: 'white', padding: '10px' }}>
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Filtro */}
      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Filtrar por placa..."
          value={searchPlaca}
          onChange={e => setSearchPlaca(e.target.value)}
          style={{ width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '4px' }}
        />
      </div>

      {/* Tabela */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{
          width: '100%',
          borderCollapse: 'collapse',
          backgroundColor: 'white',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <thead>
            <tr style={{ backgroundColor: '#f5f5f5', borderBottom: '2px solid #ddd' }}>
              <th style={{ padding: '12px', textAlign: 'left' }}>Placa</th>
              <th style={{ padding: '12px', textAlign: 'left' }}>Modelo</th>
              <th style={{ padding: '12px', textAlign: 'left' }}>Ano</th>
              <th style={{ padding: '12px', textAlign: 'left' }}>Responsavel</th>
              <th style={{ padding: '12px', textAlign: 'center' }}>Acoes</th>
            </tr>
          </thead>
          <tbody>
            {veiculosFiltrados.length > 0 ? (
              veiculosFiltrados.map(v => {
                const resp = responsaveis.find(r => r.id === v.id_responsavel)
                return (
                  <tr key={v.id_veiculo} style={{ borderBottom: '1px solid #eee', hover: { backgroundColor: '#f9f9f9' } }}>
                    <td style={{ padding: '12px' }}><strong>{v.placa}</strong></td>
                    <td style={{ padding: '12px' }}>{v.modelo || 'N/A'}</td>
                    <td style={{ padding: '12px' }}>{v.ano || 'N/A'}</td>
                    <td style={{ padding: '12px' }}>{resp ? resp.nome : 'N/A'}</td>
                    <td style={{ padding: '12px', textAlign: 'center' }}>
                      <button
                        onClick={() => editarVeiculo(v)}
                        style={{ marginRight: '8px', backgroundColor: '#2196F3', color: 'white', padding: '6px 12px', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                      >
                        Editar
                      </button>
                      <button
                        onClick={() => deletar(v.id_veiculo)}
                        style={{ backgroundColor: '#f44336', color: 'white', padding: '6px 12px', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                      >
                        Deletar
                      </button>
                    </td>
                  </tr>
                )
              })
            ) : (
              <tr>
                <td colSpan="5" style={{ padding: '20px', textAlign: 'center', color: '#999' }}>
                  Nenhum veiculo encontrado
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Info */}
      <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#e3f2fd', borderRadius: '4px', border: '1px solid #2196F3' }}>
        <strong>Total de Veiculos:</strong> {veiculos.length}
      </div>
    </div>
  )
}
