import React, { useEffect, useState } from 'react'
import api from '../api'
import FormField from '../components/FormField'
import '../styles.css'

export default function Users(){
  const [users, setUsers] = useState([])
  const [form, setForm] = useState({ id_usuario: null, nome:'', documento:'', id_tipo_usuario:'1', login:'', senha:'', id_perfil_acesso:'', empresa_origem:null, contato:'', ativo:true })
  const [lookups, setLookups] = useState({tiposUsuario:[], perfis:[], tiposEmpresa:[]})
  const [mostrando, setMostrando] = useState(false)
  const [editando, setEditando] = useState(false)

  useEffect(()=>{
    api.fetchLookups().then(l=> setLookups(l))
    api.listUsers().then(r=>{ if(r.status===200) setUsers(r.data||[]) })
  },[])

  // Verifica se é usuário interno baseado na CHAVE do tipo (admin, seguranca, operador)
  const tipoUsuarioNum = parseInt(form.id_tipo_usuario || 1)
  const tipoSelecionado = lookups.tiposUsuario?.find(t => t.id === tipoUsuarioNum)
  const tiposInternosChaves = ['admin', 'seguranca', 'operador']
  const ehInterno = tipoSelecionado && tiposInternosChaves.includes(tipoSelecionado.chave)

  async function submit(e){
    e.preventDefault()
    
    const tipo = parseInt(form.id_tipo_usuario || 1)
    const isInterno = [1, 2, 3].includes(tipo)
    
    // Validações
    if(!form.nome.trim()){
      alert('Nome é obrigatório')
      return
    }
    if(!form.documento.trim()){
      alert('Documento é obrigatório')
      return
    }
    if(isInterno && !form.login.trim()){
      alert('Login é obrigatório para usuários internos')
      return
    }
    if(isInterno && !form.senha.trim() && !editando){
      alert('Senha é obrigatória para usuários internos')
      return
    }
    if(isInterno && !form.id_perfil_acesso){
      alert('Perfil de acesso é obrigatório para usuários internos')
      return
    }

    const token = localStorage.getItem('token')
    const payload = {
      nome: form.nome,
      documento: form.documento,
      id_tipo_usuario: tipo,
      empresa_origem: form.empresa_origem ? parseInt(form.empresa_origem) : null,
      contato: form.contato || null,
      ativo: true
    }
    
    // Adicionar campos de acesso para todos (interno com valores, externo com null)
    if(isInterno){
      payload.login = form.login
      if(form.senha.trim()) payload.senha = form.senha  // Apenas se preenchido (não obrigatório na edição)
      payload.id_perfil_acesso = parseInt(form.id_perfil_acesso)
    } else {
      payload.login = null
      payload.senha = null
      payload.id_perfil_acesso = null
    }
    
    // Se está editando, fazer update, senão fazer create
    if(editando){
      const r = await api.updateUser(form.id_usuario, payload, token)
      if(r.status===200){
        alert('Usuário atualizado com sucesso!')
        // Limpar formulário
        setForm({ id_usuario: null, nome:'', documento:'', id_tipo_usuario:'1', login:'', senha:'', id_perfil_acesso:'', empresa_origem:null, contato:'', ativo:true })
        setMostrando(false)
        setEditando(false)
        // Recarregar lista
        const res = await api.listUsers()
        if(res.status===200) setUsers(res.data)
      }else{
        alert('Erro: '+(r.data?.detail||JSON.stringify(r.data)))
      }
    } else {
      const r = await api.registerUser(payload, token)
      if(r.status===201){
        alert('Usuário criado com sucesso!')
        // Limpar formulário
        setForm({ id_usuario: null, nome:'', documento:'', id_tipo_usuario:'1', login:'', senha:'', id_perfil_acesso:'', empresa_origem:null, contato:'', ativo:true })
        setMostrando(false)
        setEditando(false)
        // Recarregar lista
        const res = await api.listUsers()
        if(res.status===200) setUsers(res.data)
      }else{
        alert('Erro: '+(r.data?.detail||JSON.stringify(r.data)))
      }
    }
  }

  const novoUsuario = () => {
    setForm({ id_usuario: null, nome:'', documento:'', id_tipo_usuario:'1', login:'', senha:'', id_perfil_acesso:'', empresa_origem:null, contato:'', ativo:true })
    setMostrando(true)
    setEditando(false)
  }

  const editarUsuario = (usuario) => {
    setForm({
      id_usuario: usuario.id_usuario,
      nome: usuario.nome,
      documento: usuario.documento,
      id_tipo_usuario: String(usuario.id_tipo_usuario),
      login: usuario.login || '',
      senha: '',
      id_perfil_acesso: usuario.id_perfil_acesso || '',
      empresa_origem: usuario.empresa_origem,
      contato: usuario.contato || '',
      ativo: usuario.ativo
    })
    setMostrando(true)
    setEditando(true)
  }

  const excluirUsuario = async (usuarioId) => {
    if(!window.confirm('Tem certeza que deseja excluir este usuário?')) return
    
    const token = localStorage.getItem('token')
    try {
      const res = await api.deleteUser(usuarioId, token)
      if(res.status === 200){
        alert('Usuário excluído com sucesso!')
        const updatedUsers = users.filter(u => u.id_usuario !== usuarioId)
        setUsers(updatedUsers)
      }
    } catch(err){
      alert('Erro ao excluir: ' + (err.message || JSON.stringify(err)))
    }
  }

  const cancelar = () => {
    setMostrando(false)
    setEditando(false)
    setForm({ id_usuario: null, nome:'', documento:'', id_tipo_usuario:'1', login:'', senha:'', id_perfil_acesso:'', empresa_origem:null, contato:'', ativo:true })
  }

  return (
    <div className="users-container">
      <h2>Gestão de Usuários</h2>
      
      <button 
        onClick={novoUsuario}
        className="btn-novo-usuario"
      >
        + Novo Usuário
      </button>

      {mostrando && (
        <form onSubmit={submit} className="users-form">
          <h3>{editando ? `Editar Usuário #${form.id_usuario}` : 'Cadastrar Novo Usuário'}</h3>
          
          <div className="form-grid">
            <FormField label="Nome *">
              <input 
                value={form.nome} 
                onChange={e=>setForm({...form,nome:e.target.value})} 
                placeholder="Nome completo"
                required 
              />
            </FormField>

            <FormField label="Documento *">
              <input 
                value={form.documento} 
                onChange={e=>setForm({...form,documento:e.target.value})} 
                placeholder="CPF ou documento"
                required 
              />
            </FormField>

            <FormField label="Tipo de Usuário *">
              <select 
                value={form.id_tipo_usuario} 
                onChange={e=>setForm({...form,id_tipo_usuario:e.target.value})}
              >
                { (lookups.tiposUsuario||[]).length ? (lookups.tiposUsuario.map(t=> <option key={t.id} value={String(t.id)}>{t.nome}</option>)) : (<option value="1">Interno</option>) }
              </select>
            </FormField>

            {ehInterno && (
              <>
                <FormField label="Login *">
                  <input 
                    value={form.login} 
                    onChange={e=>setForm({...form,login:e.target.value})} 
                    placeholder="Login para acesso ao sistema"
                    required
                  />
                </FormField>

                <FormField label="Senha *">
                  <input 
                    type="password"
                    value={form.senha} 
                    onChange={e=>setForm({...form,senha:e.target.value})} 
                    placeholder="Mínimo 6 caracteres"
                    required
                  />
                </FormField>

                <FormField label="Perfil de Acesso *">
                  <select 
                    value={form.id_perfil_acesso} 
                    onChange={e=>setForm({...form,id_perfil_acesso:e.target.value})}
                    required
                  >
                    <option value="">Selecione um perfil...</option>
                    { (lookups.perfis||[]).length ? (lookups.perfis.map(p=> <option key={p.id} value={p.id}>{p.nome}</option>)) : (<><option value={1}>Porteiro</option><option value={2}>Admin</option></>) }
                  </select>
                </FormField>
              </>
            )}

            <FormField label="Empresa Origem">
              <select 
                value={form.empresa_origem||''} 
                onChange={e=>setForm({...form,empresa_origem: e.target.value?parseInt(e.target.value):null})}
              >
                <option value="">(nenhuma)</option>
                { (lookups.tiposEmpresa||[]).map(t=> <option key={t.id} value={t.id}>{t.nome}</option>) }
              </select>
            </FormField>

            <FormField label="Contato">
              <input 
                value={form.contato} 
                onChange={e=>setForm({...form,contato:e.target.value})} 
                placeholder="Telefone ou email"
              />
            </FormField>
          </div>

          {!ehInterno && (
            <div className="warning-box">
              <strong>⚠️ Usuários externos</strong><br/>
              <small>Visitantes e Terceiros não possuem acesso ao sistema. Apenas informações de entrada/saída serão registradas.</small>
            </div>
          )}

          <div className="form-buttons">
            <button 
              type="submit"
              className="btn-submit"
            >
              {editando ? 'Atualizar Usuário' : 'Criar Usuário'}
            </button>
            <button 
              type="button"
              onClick={cancelar}
              className="btn-cancel"
            >
              Cancelar
            </button>
          </div>
        </form>
      )}

      <h3 style={{ marginTop:'30px', marginBottom:'15px' }}>Usuários Existentes</h3>
      
      <div className="table-responsive">
        <table className="users-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>Login</th>
              <th>Documento</th>
              <th>Ativo</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {users.length > 0 ? users.map(u=> (
              <tr key={u.id_usuario}>
                <td data-label="ID">{u.id_usuario}</td>
                <td data-label="Nome">{u.nome}</td>
                <td data-label="Login">{u.login || '-'}</td>
                <td data-label="Documento">{u.documento}</td>
                <td data-label="Ativo">{u.ativo ? 'Sim' : 'Não'}</td>
                <td data-label="Ações" className="acoes-cell">
                  <button
                    onClick={() => editarUsuario(u)}
                    className="btn-editar"
                    title="Editar"
                  >
                    ✏️ Editar
                  </button>
                  <button
                    onClick={() => excluirUsuario(u.id_usuario)}
                    className="btn-excluir"
                    title="Excluir"
                  >
                    🗑️ Excluir
                  </button>
                </td>
              </tr>
            )) : (
              <tr>
                <td colSpan="6" style={{ textAlign:'center', padding:'30px', color:'#999' }}>
                  Nenhum usuário cadastrado
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
