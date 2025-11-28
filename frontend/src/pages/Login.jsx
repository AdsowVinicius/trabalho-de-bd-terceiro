import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'
import FormField from '../components/FormField'
import '../styles.css'

export default function Login(){
  const [login, setLogin] = useState('')
  const [senha, setSenha] = useState('')
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)
  const [perfis, setPerfis] = useState([])
  const [loadingPerfis, setLoadingPerfis] = useState(true)
  const [logging, setLogging] = useState(false)
  const nav = useNavigate()

  useEffect(()=>{
    api.fetchLookups().then(l=>{ if(l.perfis) setPerfis(l.perfis); setLoadingPerfis(false) }).catch(()=>setLoadingPerfis(false))
  },[])

  async function doLogin(e){
    e.preventDefault()
    setError(null)
    setSuccess(null)
    setLogging(true)
    
    if(loadingPerfis){
      setError('⏳ Aguarde, carregando dados necessários...')
      setLogging(false)
      return
    }
    
    const r = await api.login({ login, senha })
    
    if(r.status === 200){
      const token = r.data.access_token
      const usuario = r.data.usuario
      const perfilId = usuario.id_perfil_acesso
      const perfilObj = perfis.find(p=>p.id===perfilId || p.id_perfil_acesso===perfilId || p.value===perfilId)
      const perfilNome = perfilObj ? (perfilObj.nome || perfilObj.label || perfilObj.value) : null
      const allowedPerfils = ['porteiro', 'funcionário', 'funcionario', 'administrador', 'admin', 'segurança', 'seguranca']
      
      if(perfilNome && allowedPerfils.some(p => perfilNome.toLowerCase().includes(p))){
        setSuccess('✅ Autenticação bem-sucedida! Redirecionando...')
        localStorage.setItem('token', token)
        localStorage.setItem('usuario', JSON.stringify(usuario))
        setTimeout(() => nav('/controle-acesso'), 500)
      }else{
        setError('❌ Usuário não autorizado a usar este painel')
        setLogging(false)
      }
    }else{
      const msg = (r.data && (r.data.detail || r.data.message || r.data.error)) || 'Erro ao autenticar'
      setError('❌ ' + msg)
      setLogging(false)
    }
  }

  return (
    <div className="login-container">
      {/* Background Pattern */}
      <div className="login-background">
        <div className="login-pattern-circle-1"></div>
        <div className="login-pattern-circle-2"></div>
        <div className="login-pattern-circle-3"></div>
      </div>

      {/* Main Content */}
      <div className="login-wrapper">
        {/* Logo Section */}
        <div className="login-header">
          <div className="login-logo">
            <span className="login-logo-icon">🔐</span>
          </div>
          <h1>Central de Acesso</h1>
          <p className="login-subtitle">Sistema de Controle de Acesso TERCEIRIZE+</p>
        </div>

        {/* Form Card */}
        <div className="login-form-card">
          {/* Success Message */}
          {success && (
            <div className="login-alert login-alert-success">
              {success}
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="login-alert login-alert-error">
              {error}
            </div>
          )}

          <form onSubmit={doLogin} className="login-form">
            <div className="login-form-group">
              <FormField label="Usuário" required>
                <input 
                  type="text"
                  value={login} 
                  onChange={e=>setLogin(e.target.value)} 
                  placeholder="Digite seu usuário"
                  disabled={logging}
                  required 
                />
              </FormField>
            </div>

            <div className="login-form-group">
              <FormField label="Senha" required>
                <input 
                  type="password"
                  value={senha} 
                  onChange={e=>setSenha(e.target.value)} 
                  placeholder="Digite sua senha"
                  disabled={logging}
                  required 
                />
              </FormField>
            </div>

            <button 
              type="submit" 
              disabled={loadingPerfis || logging}
              className="login-submit-button"
            >
              {logging ? '⏳ Autenticando...' : loadingPerfis ? '⏳ Carregando...' : '🚀 Entrar'}
            </button>
          </form>

          {/* Footer Info */}
          <div className="login-footer">
            <p className="login-info-text">
              <strong>👥 Acesso para:</strong> Porteiros, Funcionários, Administradores e Segurança
            </p>
            <div className="login-features">
              <div className="login-feature">
                <span className="login-feature-icon">📋</span>
                <span>Monitoramento</span>
              </div>
              <div className="login-feature">
                <span className="login-feature-icon">🚗</span>
                <span>Veículos</span>
              </div>
              <div className="login-feature">
                <span className="login-feature-icon">👤</span>
                <span>Usuários</span>
              </div>
              <div className="login-feature">
                <span className="login-feature-icon">🏢</span>
                <span>Empresas</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Info Section */}
        <div className="login-info-section">
          <div className="login-info-card">
            <h3>🔒 Seguro</h3>
            <p>Autenticação com JWT e criptografia de senha</p>
          </div>
          <div className="login-info-card">
            <h3>⚡ Rápido</h3>
            <p>Interface responsiva e otimizada para todos os dispositivos</p>
          </div>
          <div className="login-info-card">
            <h3>📊 Completo</h3>
            <p>Sistema completo de gestão de acessos</p>
          </div>
        </div>
      </div>
    </div>
  )
}
