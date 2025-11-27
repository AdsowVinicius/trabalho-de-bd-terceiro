import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'
import FormField from '../components/FormField'

export default function AcessoPessoal(){
  const [form, setForm] = useState({ id_usuario:'', documento_usuario:'', id_tipo_acesso:1, id_empresa_visitada:null, motivo_visita:'', observacao:'' })
  const [lookups, setLookups] = useState({ tiposServico:[], empresas:[] })
  const [usuarios, setUsuarios] = useState([])
  const [usuariosFiltrados, setUsuariosFiltrados] = useState([])
  const [empresasFiltradas, setEmpresasFiltradas] = useState([])
  const [usuarioSelecionado, setUsuarioSelecionado] = useState(null)
  const [empresaSelecionada, setEmpresaSelecionada] = useState(null)
  const [showUsuariosList, setShowUsuariosList] = useState(false)
  const [showEmpresasList, setShowEmpresasList] = useState(false)
  const [showNovoUsuario, setShowNovoUsuario] = useState(false)
  const [searchUsuario, setSearchUsuario] = useState('')
  const [searchEmpresa, setSearchEmpresa] = useState('')
  const token = localStorage.getItem('token')
  const nav = useNavigate()

  useEffect(()=>{
    api.fetchLookups().then(l=> setLookups({ tiposServico: l.tiposServico||[], empresas: l.empresas||[] }))
    api.listUsers().then(r=>{ if(r.status===200) setUsuarios(r.data||[]) })
  },[])

  // Filtrar usuários por nome ou documento
  const handleSearchUsuario = (valor) => {
    setSearchUsuario(valor)
    if(valor.trim()){
      const filtrados = usuarios.filter(u=>
        u.nome.toLowerCase().includes(valor.toLowerCase()) ||
        u.documento.includes(valor) ||
        u.login.toLowerCase().includes(valor.toLowerCase())
      )
      setUsuariosFiltrados(filtrados)
      setShowUsuariosList(true)
    } else {
      setUsuariosFiltrados([])
      setShowUsuariosList(false)
    }
  }

  // Filtrar empresas por nome
  const handleSearchEmpresa = (valor) => {
    setSearchEmpresa(valor)
    if(valor.trim()){
      const filtradas = (lookups.empresas||[]).filter(e=>
        e.nome.toLowerCase().includes(valor.toLowerCase())
      )
      setEmpresasFiltradas(filtradas)
      setShowEmpresasList(true)
    } else {
      setEmpresasFiltradas([])
      setShowEmpresasList(false)
    }
  }

  // Selecionar usuário
  const selecionarUsuario = (usuario) => {
    setUsuarioSelecionado(usuario)
    setForm({...form, id_usuario: usuario.id_usuario, documento_usuario: usuario.documento})
    setSearchUsuario(`${usuario.nome} (${usuario.documento})`)
    setShowUsuariosList(false)
  }

  // Selecionar empresa
  const selecionarEmpresa = (empresa) => {
    setEmpresaSelecionada(empresa)
    setForm({...form, id_empresa_visitada: empresa.id})
    setSearchEmpresa(empresa.nome)
    setShowEmpresasList(false)
  }

  async function submit(e){
    e.preventDefault()
    if(!usuarioSelecionado){
      alert('Por favor, selecione um usuário')
      return
    }
    const r = await api.createAcessoPessoal(form, token)
    if(r.status===201){ 
      alert('Acesso pessoal registrado com sucesso')
      setForm({ id_usuario:'', documento_usuario:'', id_tipo_acesso:1, id_empresa_visitada:null, motivo_visita:'', observacao:'' })
      setUsuarioSelecionado(null)
      setEmpresaSelecionada(null)
      setSearchUsuario('')
      setSearchEmpresa('')
    }
    else alert('Erro: '+(r.data?.detail||JSON.stringify(r.data)))
  }

  return (
    <div style={{ maxWidth:900, margin:'20px auto' }}>
      <h2>Registrar Acesso Pessoal</h2>
      
      <form onSubmit={submit}>
        {/* Campo de Usuário com Busca */}
        <FormField label="Pesquisar Usuário">
          <div style={{ position:'relative' }}>
            <input 
              type="text"
              placeholder="Digite nome, documento ou login do usuário"
              value={searchUsuario}
              onChange={e=>handleSearchUsuario(e.target.value)}
              onFocus={()=>searchUsuario.trim() && setShowUsuariosList(true)}
            />
            {showUsuariosList && (
              <div style={{ 
                position:'absolute', 
                top:'100%', 
                left:0, 
                right:0, 
                border:'1px solid #ddd', 
                maxHeight:'200px', 
                overflowY:'auto',
                backgroundColor:'white',
                zIndex:10
              }}>
                {usuariosFiltrados.length > 0 ? (
                  usuariosFiltrados.map(u=>
                    <div 
                      key={u.id_usuario}
                      onClick={()=>selecionarUsuario(u)}
                      style={{ padding:'8px', borderBottom:'1px solid #eee', cursor:'pointer', backgroundColor: usuarioSelecionado?.id_usuario===u.id_usuario?'#e3f2fd':'white' }}
                    >
                      <strong>{u.nome}</strong> ({u.documento}) - {u.login}
                    </div>
                  )
                ) : (
                  <div style={{ padding:'8px', color:'#999' }}>Nenhum usuário encontrado</div>
                )}
              </div>
            )}
          </div>
          {usuarioSelecionado && (
            <button type="button" onClick={()=>{setUsuarioSelecionado(null); setSearchUsuario(''); setForm({...form, id_usuario:'', documento_usuario:''}); }} style={{ marginTop:'8px' }}>
              Limpar Seleção
            </button>
          )}
        </FormField>

        {/* Documento do Usuário (apenas leitura) */}
        {usuarioSelecionado && (
          <FormField label="Documento do Usuário">
            <input type="text" value={form.documento_usuario} disabled />
          </FormField>
        )}

        {/* Tipo de Acesso */}
        <FormField label="Tipo de Acesso">
          <select value={form.id_tipo_acesso} onChange={e=>setForm({...form,id_tipo_acesso:parseInt(e.target.value)})}>
            {(lookups.tiposServico||[]).length ? lookups.tiposServico.map(t=> <option key={t.id} value={t.id}>{t.nome}</option>) : <option value={1}>Visita</option> }
          </select>
        </FormField>

        {/* Campo de Empresa com Busca */}
        <FormField label="Pesquisar Empresa Visitada">
          <div style={{ position:'relative' }}>
            <input 
              type="text"
              placeholder="Digite o nome da empresa (opcional)"
              value={searchEmpresa}
              onChange={e=>handleSearchEmpresa(e.target.value)}
              onFocus={()=>searchEmpresa.trim() && setShowEmpresasList(true)}
            />
            {showEmpresasList && (
              <div style={{ 
                position:'absolute', 
                top:'100%', 
                left:0, 
                right:0, 
                border:'1px solid #ddd', 
                maxHeight:'200px', 
                overflowY:'auto',
                backgroundColor:'white',
                zIndex:10
              }}>
                {empresasFiltradas.length > 0 ? (
                  empresasFiltradas.map(e=>
                    <div 
                      key={e.id}
                      onClick={()=>selecionarEmpresa(e)}
                      style={{ padding:'8px', borderBottom:'1px solid #eee', cursor:'pointer', backgroundColor: empresaSelecionada?.id===e.id?'#e3f2fd':'white' }}
                    >
                      {e.nome}
                    </div>
                  )
                ) : (
                  <div style={{ padding:'8px', color:'#999' }}>Nenhuma empresa encontrada</div>
                )}
              </div>
            )}
          </div>
          {empresaSelecionada && (
            <button type="button" onClick={()=>{setEmpresaSelecionada(null); setSearchEmpresa(''); setForm({...form, id_empresa_visitada:null}); }} style={{ marginTop:'8px' }}>
              Limpar Seleção
            </button>
          )}
        </FormField>

        {/* Motivo da Visita */}
        <FormField label="Motivo da Visita">
          <input 
            value={form.motivo_visita} 
            onChange={e=>setForm({...form,motivo_visita:e.target.value})}
            placeholder="Ex: Apresentação comercial, Reunião, etc"
          />
        </FormField>

        {/* Observação */}
        <FormField label="Observação">
          <textarea 
            value={form.observacao} 
            onChange={e=>setForm({...form,observacao:e.target.value})}
            placeholder="Informações adicionais"
            rows={4}
          />
        </FormField>

        {/* Botões de Ação */}
        <div style={{ display:'flex', gap:'10px', marginTop:'20px' }}>
          <button type="submit" disabled={!usuarioSelecionado} style={{ flex:1 }}>
            Registrar Acesso
          </button>
          <button 
            type="button" 
            onClick={()=>setShowNovoUsuario(!showNovoUsuario)}
            style={{ flex:1, backgroundColor:'#ff9800' }}
          >
            {showNovoUsuario ? 'Cancelar' : 'Cadastrar Novo Usuário'}
          </button>
        </div>
      </form>

      {/* Modal/Formulário de Novo Usuário */}
      {showNovoUsuario && (
        <div style={{ marginTop:'30px', border:'2px solid #ff9800', padding:'20px', borderRadius:'8px', backgroundColor:'#fff3e0' }}>
          <h3>Cadastrar Novo Usuário</h3>
          <p style={{ color:'#666' }}>Preencha os dados do novo usuário e ele será adicionado ao sistema</p>
          <button 
            type="button"
            onClick={()=>nav('/users')}
            style={{ width:'100%', padding:'12px', backgroundColor:'#4CAF50', color:'white', border:'none', borderRadius:'4px', cursor:'pointer', fontSize:'16px' }}
          >
            Ir para Gestão de Usuários
          </button>
        </div>
      )}
    </div>
  )
}
