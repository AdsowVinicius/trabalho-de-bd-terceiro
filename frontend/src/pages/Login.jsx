import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'
import FormField from '../components/FormField'

export default function Login(){
  const [login, setLogin] = useState('')
  const [senha, setSenha] = useState('')
  const [error, setError] = useState(null)
  const [perfis, setPerfis] = useState([])
  const [loadingPerfis, setLoadingPerfis] = useState(true)
  const nav = useNavigate()

  useEffect(()=>{
    api.fetchLookups().then(l=>{ if(l.perfis) setPerfis(l.perfis); setLoadingPerfis(false) }).catch(()=>setLoadingPerfis(false))
  },[])

  async function doLogin(e){
    e.preventDefault()
    setError(null)
    if(loadingPerfis){
      setError('Aguarde, carregando dados necessários...')
      return
    }
    const r = await api.login({ login, senha })
    if(r.status === 200){
      // r.data has access_token and usuario
      const token = r.data.access_token
      const usuario = r.data.usuario
      // Allow users with perfils: Porteiro, Funcionário, Administrador, Segurança
      const perfilId = usuario.id_perfil_acesso
      const perfilObj = perfis.find(p=>p.id===perfilId || p.id_perfil_acesso===perfilId || p.value===perfilId)
      const perfilNome = perfilObj ? (perfilObj.nome || perfilObj.label || perfilObj.value) : null
      const allowedPerfils = ['porteiro', 'funcionário', 'funcionario', 'administrador', 'admin', 'segurança', 'seguranca']
      if(perfilNome && allowedPerfils.some(p => perfilNome.toLowerCase().includes(p))){
        localStorage.setItem('token', token)
        localStorage.setItem('usuario', JSON.stringify(usuario))
        nav('/acessos-pessoais')
      }else{
        setError('Usuário não autorizado a usar este painel')
      }
    }else{
      // Show backend error message when available
      const msg = (r.data && (r.data.detail || r.data.message || r.data.error)) || 'Erro ao autenticar'
      setError(msg)
    }
  }

  return (
    <div style={{ maxWidth:600, margin:'20px auto' }}>
      <h2>Login - Painel de Acesso</h2>
      <form onSubmit={doLogin}>
        <FormField label="Login">
          <input value={login} onChange={e=>setLogin(e.target.value)} required />
        </FormField>
        <FormField label="Senha">
          <input type="password" value={senha} onChange={e=>setSenha(e.target.value)} required />
        </FormField>
        <div>
          <button type="submit" disabled={loadingPerfis}>{loadingPerfis? 'Carregando...' : 'Entrar'}</button>
        </div>
        {error && <div style={{ marginTop: 12, color:'red' }}>{error}</div>}
      </form>
      <p style={{ marginTop:20, color:'#666' }}>Acesso para: Porteiro, Funcionário, Administrador e Segurança.</p>
    </div>
  )
}
