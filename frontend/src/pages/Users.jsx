import React, { useEffect, useState } from 'react'
import api from '../api'
import FormField from '../components/FormField'

export default function Users(){
  const [users, setUsers] = useState([])
  const [form, setForm] = useState({ nome:'', documento:'', id_tipo_usuario:1, login:'', senha:'', id_perfil_acesso:1, empresa_origem:null, contato:'', ativo:true })
  const [lookups, setLookups] = useState({tiposUsuario:[], perfis:[], tiposEmpresa:[]})

  useEffect(()=>{
    api.fetchLookups().then(l=> setLookups(l))
    api.listUsers().then(r=>{ if(r.status===200) setUsers(r.data||[]) })
  },[])

  async function submit(e){
    e.preventDefault()
    const token = localStorage.getItem('token')
    const r = await api.registerUser(form, token)
    if(r.status===201){
      alert('Usuário criado')
      const res = await api.listUsers()
      if(res.status===200) setUsers(res.data)
    }else{
      alert('Erro: '+(r.data?.detail||JSON.stringify(r.data)))
    }
  }

  return (
    <div style={{ maxWidth:900, margin:'20px auto' }}>
      <h2>Gestão de Usuários</h2>
      <form onSubmit={submit} style={{ border:'1px solid #ddd', padding:12 }}>
        <FormField label="Nome"><input value={form.nome} onChange={e=>setForm({...form,nome:e.target.value})} required /></FormField>
        <FormField label="Documento"><input value={form.documento} onChange={e=>setForm({...form,documento:e.target.value})} required /></FormField>
        <FormField label="Tipo de Usuário">
          <select value={form.id_tipo_usuario} onChange={e=>setForm({...form,id_tipo_usuario:parseInt(e.target.value)})}>
            { (lookups.tiposUsuario||[]).length ? (lookups.tiposUsuario.map(t=> <option key={t.id} value={t.id}>{t.nome}</option>)) : (<option value={1}>Interno</option>) }
          </select>
        </FormField>
        <FormField label="Login"><input value={form.login} onChange={e=>setForm({...form,login:e.target.value})} required /></FormField>
        <FormField label="Senha"><input type="password" value={form.senha} onChange={e=>setForm({...form,senha:e.target.value})} required /></FormField>
        <FormField label="Perfil de Acesso">
          <select value={form.id_perfil_acesso} onChange={e=>setForm({...form,id_perfil_acesso:parseInt(e.target.value)})}>
            { (lookups.perfis||[]).length ? (lookups.perfis.map(p=> <option key={p.id} value={p.id}>{p.nome}</option>)) : (<><option value={1}>Porteiro</option><option value={2}>Admin</option></>) }
          </select>
        </FormField>
        <FormField label="Empresa Origem">
          <select value={form.empresa_origem||''} onChange={e=>setForm({...form,empresa_origem: e.target.value?parseInt(e.target.value):null})}>
            <option value="">(nenhuma)</option>
            { (lookups.tiposEmpresa||[]).map(t=> <option key={t.id} value={t.id}>{t.nome}</option>) }
          </select>
        </FormField>
        <FormField label="Contato"><input value={form.contato} onChange={e=>setForm({...form,contato:e.target.value})} /></FormField>
        <div><button type="submit">Criar Usuário</button></div>
      </form>

      <h3 style={{ marginTop:20 }}>Usuários existentes</h3>
      <table style={{ width:'100%', borderCollapse:'collapse' }}>
        <thead><tr><th>id</th><th>nome</th><th>login</th><th>documento</th><th>ativo</th></tr></thead>
        <tbody>
          {users.map(u=> (
            <tr key={u.id_usuario}><td>{u.id_usuario}</td><td>{u.nome}</td><td>{u.login}</td><td>{u.documento}</td><td>{String(u.ativo)}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
