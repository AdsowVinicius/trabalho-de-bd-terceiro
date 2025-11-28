import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Empresas(){
  const [empresas, setEmpresas] = useState([])
  const [tiposEmpresa, setTiposEmpresa] = useState([])
  const [form, setForm] = useState({ nome_empresa:'', cnpj:'', id_tipo_empresa:'', responsavel:'', contato:'' })
  const [editando, setEditando] = useState(false)
  const [mostrando, setMostrando] = useState(false)
  const [filtro, setFiltro] = useState('')
  
  const token = localStorage.getItem('token')
  const nav = useNavigate()

  useEffect(()=>{
    carregarEmpresas()
    carregarTiposEmpresa()
  }, [])

  const carregarEmpresas = async () => {
    try{
      const res = await fetch('http://127.0.0.1:8001/empresas/', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if(res.ok){
        const dados = await res.json()
        setEmpresas(dados)
      }
    }catch(e){
      console.error('Erro ao carregar empresas:', e)
    }
  }

  const carregarTiposEmpresa = async () => {
    try{
      const res = await fetch('http://127.0.0.1:8001/lookups/tipos-empresa', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if(res.ok){
        const dados = await res.json()
        setTiposEmpresa(dados)
      }
    }catch(e){
      console.error('Erro ao carregar tipos empresa:', e)
    }
  }

  const novaEmpresa = () => {
    setForm({ nome_empresa:'', cnpj:'', id_tipo_empresa:'', responsavel:'', contato:'' })
    setEditando(false)
    setMostrando(true)
  }

  const editarEmpresa = (empresa) => {
    setForm(empresa)
    setEditando(true)
    setMostrando(true)
  }

  const salvar = async (e) => {
    e.preventDefault()
    
    const nomeEmpresaTrimado = form.nome_empresa.trim()
    if(!nomeEmpresaTrimado){
      alert('Nome da empresa é obrigatório')
      return
    }
    if(nomeEmpresaTrimado.length < 3){
      alert('Nome da empresa deve ter no mínimo 3 caracteres')
      return
    }
    if(nomeEmpresaTrimado.length > 120){
      alert('Nome da empresa não pode exceder 120 caracteres')
      return
    }
    
    const cnpjTrimado = form.cnpj.trim().replace(/\D/g, '')
    if(!cnpjTrimado){
      alert('CNPJ é obrigatório')
      return
    }
    if(cnpjTrimado.length !== 14){
      alert('CNPJ deve conter 14 dígitos')
      return
    }
    
    if(!form.id_tipo_empresa){
      alert('Tipo de empresa é obrigatório')
      return
    }
    
    const responsavelTrimado = form.responsavel.trim()
    const contatoTrimado = form.contato.trim()

    try{
      const url = editando 
        ? `http://127.0.0.1:8001/empresas/${form.id_empresa}`
        : 'http://127.0.0.1:8001/empresas/'
      
      const method = editando ? 'PUT' : 'POST'

      const res = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          nome_empresa: nomeEmpresaTrimado,
          cnpj: cnpjTrimado,
          id_tipo_empresa: parseInt(form.id_tipo_empresa),
          responsavel: responsavelTrimado && responsavelTrimado.length > 0 ? responsavelTrimado : null,
          contato: contatoTrimado && contatoTrimado.length > 0 ? contatoTrimado : null
        })
      })

      if(res.ok){
        alert(editando ? 'Empresa atualizada com sucesso!' : 'Empresa criada com sucesso!')
        cancelar()
        carregarEmpresas()
      }else{
        const erro = await res.json()
        alert('Erro: ' + (erro.detail || 'Falha na operação'))
      }
    }catch(e){
      alert('Erro ao salvar empresa: ' + e.message)
    }
  }

  const deletar = async (id) => {
    if(window.confirm('Tem certeza que deseja deletar esta empresa?')){
      try{
        const res = await fetch(`http://127.0.0.1:8001/empresas/${id}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if(res.ok){
          alert('Empresa deletada com sucesso!')
          carregarEmpresas()
        }else{
          const erro = await res.json()
          alert('Erro: ' + (erro.detail || 'Falha ao deletar'))
        }
      }catch(e){
        alert('Erro ao deletar empresa: ' + e.message)
      }
    }
  }

  const cancelar = () => {
    setForm({ nome_empresa:'', cnpj:'', id_tipo_empresa:'', responsavel:'', contato:'' })
    setEditando(false)
    setMostrando(false)
  }

  const empresasFiltradas = empresas.filter(e => 
    e.nome_empresa.toLowerCase().includes(filtro.toLowerCase()) ||
    e.cnpj.includes(filtro)
  )

  const getNomeTipo = (id) => {
    const tipo = tiposEmpresa.find(t => t.id === id)
    return tipo ? tipo.nome : '-'
  }

  return (
    <div style={{ maxWidth:1000, margin:'20px auto', padding:'20px' }}>
      <h2>Gestão de Empresas</h2>
      
      <button onClick={novaEmpresa} style={{ marginBottom:'20px', padding:'10px 20px', backgroundColor:'#2196F3', color:'#fff', border:'none', borderRadius:'4px', cursor:'pointer' }}>
        Nova Empresa
      </button>

      {mostrando && (
        <div style={{ backgroundColor:'#f5f5f5', padding:'20px', marginBottom:'20px', borderRadius:'4px' }}>
          <h3>{editando ? 'Editar Empresa' : 'Cadastrar Empresa'}</h3>
          
          <form onSubmit={salvar}>
            <div style={{ marginBottom:'15px' }}>
              <label style={{ display:'block', marginBottom:'5px', fontWeight:'bold' }}>Nome da Empresa *</label>
              <input 
                type="text"
                value={form.nome_empresa}
                onChange={e => setForm({...form, nome_empresa: e.target.value})}
                placeholder="Nome completo da empresa"
                style={{ width:'100%', padding:'8px', border:'1px solid #ddd', borderRadius:'4px', boxSizing:'border-box' }}
              />
            </div>

            <div style={{ marginBottom:'15px' }}>
              <label style={{ display:'block', marginBottom:'5px', fontWeight:'bold' }}>CNPJ *</label>
              <input 
                type="text"
                value={form.cnpj}
                onChange={e => setForm({...form, cnpj: e.target.value})}
                placeholder="00.000.000/0000-00"
                style={{ width:'100%', padding:'8px', border:'1px solid #ddd', borderRadius:'4px', boxSizing:'border-box' }}
              />
            </div>

            <div style={{ marginBottom:'15px' }}>
              <label style={{ display:'block', marginBottom:'5px', fontWeight:'bold' }}>Tipo de Empresa *</label>
              <select
                value={form.id_tipo_empresa}
                onChange={e => setForm({...form, id_tipo_empresa: e.target.value})}
                style={{ width:'100%', padding:'8px', border:'1px solid #ddd', borderRadius:'4px', boxSizing:'border-box' }}
              >
                <option value="">Selecione um tipo...</option>
                {tiposEmpresa.map(tipo => (
                  <option key={tipo.id} value={tipo.id}>{tipo.nome}</option>
                ))}
              </select>
            </div>

            <div style={{ marginBottom:'15px' }}>
              <label style={{ display:'block', marginBottom:'5px', fontWeight:'bold' }}>Responsável</label>
              <input 
                type="text"
                value={form.responsavel || ''}
                onChange={e => setForm({...form, responsavel: e.target.value})}
                placeholder="Nome do responsável"
                style={{ width:'100%', padding:'8px', border:'1px solid #ddd', borderRadius:'4px', boxSizing:'border-box' }}
              />
            </div>

            <div style={{ marginBottom:'15px' }}>
              <label style={{ display:'block', marginBottom:'5px', fontWeight:'bold' }}>Contato</label>
              <input 
                type="text"
                value={form.contato || ''}
                onChange={e => setForm({...form, contato: e.target.value})}
                placeholder="Telefone ou email"
                style={{ width:'100%', padding:'8px', border:'1px solid #ddd', borderRadius:'4px', boxSizing:'border-box' }}
              />
            </div>

            <div style={{ display:'flex', gap:'10px' }}>
              <button type="submit" style={{ flex:1, padding:'10px', backgroundColor:'#4CAF50', color:'#fff', border:'none', borderRadius:'4px', cursor:'pointer' }}>
                {editando ? 'Atualizar' : 'Salvar'}
              </button>
              <button type="button" onClick={cancelar} style={{ flex:1, padding:'10px', backgroundColor:'#f44336', color:'#fff', border:'none', borderRadius:'4px', cursor:'pointer' }}>
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      <div style={{ marginBottom:'20px' }}>
        <input 
          type="text"
          placeholder="Filtrar por nome ou CNPJ..."
          value={filtro}
          onChange={e => setFiltro(e.target.value)}
          style={{ width:'100%', padding:'10px', border:'1px solid #ddd', borderRadius:'4px', boxSizing:'border-box' }}
        />
      </div>

      <div style={{ backgroundColor:'#f9f9f9', padding:'10px', marginBottom:'20px', borderRadius:'4px' }}>
        <strong>Total de empresas: {empresasFiltradas.length}</strong>
      </div>

      <table style={{ width:'100%', borderCollapse:'collapse', backgroundColor:'#fff' }}>
        <thead>
          <tr style={{ backgroundColor:'#f0f0f0', borderBottom:'2px solid #ddd' }}>
            <th style={{ padding:'12px', textAlign:'left', borderRight:'1px solid #ddd' }}>Nome</th>
            <th style={{ padding:'12px', textAlign:'left', borderRight:'1px solid #ddd' }}>CNPJ</th>
            <th style={{ padding:'12px', textAlign:'left', borderRight:'1px solid #ddd' }}>Tipo</th>
            <th style={{ padding:'12px', textAlign:'left', borderRight:'1px solid #ddd' }}>Responsável</th>
            <th style={{ padding:'12px', textAlign:'left', borderRight:'1px solid #ddd' }}>Contato</th>
            <th style={{ padding:'12px', textAlign:'center' }}>Ações</th>
          </tr>
        </thead>
        <tbody>
          {empresasFiltradas.length > 0 ? empresasFiltradas.map(empresa => (
            <tr key={empresa.id_empresa} style={{ borderBottom:'1px solid #ddd', '&:hover': { backgroundColor:'#f5f5f5' } }}>
              <td style={{ padding:'12px', borderRight:'1px solid #ddd' }}>{empresa.nome_empresa}</td>
              <td style={{ padding:'12px', borderRight:'1px solid #ddd' }}>{empresa.cnpj}</td>
              <td style={{ padding:'12px', borderRight:'1px solid #ddd' }}>{getNomeTipo(empresa.id_tipo_empresa)}</td>
              <td style={{ padding:'12px', borderRight:'1px solid #ddd' }}>{empresa.responsavel || '-'}</td>
              <td style={{ padding:'12px', borderRight:'1px solid #ddd' }}>{empresa.contato || '-'}</td>
              <td style={{ padding:'12px', textAlign:'center', display:'flex', gap:'8px', justifyContent:'center' }}>
                <button 
                  onClick={() => editarEmpresa(empresa)}
                  style={{ padding:'6px 12px', backgroundColor:'#ff9800', color:'#fff', border:'none', borderRadius:'3px', cursor:'pointer', fontSize:'12px' }}
                >
                  Editar
                </button>
                <button 
                  onClick={() => deletar(empresa.id_empresa)}
                  style={{ padding:'6px 12px', backgroundColor:'#f44336', color:'#fff', border:'none', borderRadius:'3px', cursor:'pointer', fontSize:'12px' }}
                >
                  Deletar
                </button>
              </td>
            </tr>
          )) : (
            <tr>
              <td colSpan="6" style={{ padding:'20px', textAlign:'center', color:'#999' }}>Nenhuma empresa encontrada</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
