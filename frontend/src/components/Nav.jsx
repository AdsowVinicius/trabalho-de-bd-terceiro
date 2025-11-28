import React from 'react'
import { Link, useNavigate } from 'react-router-dom'

export default function Nav(){
  const nav = useNavigate()
  const token = localStorage.getItem('token')
  const usuario = localStorage.getItem('usuario')
  
  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('usuario')
    nav('/login')
  }

  // Só mostra navbar se estiver logado
  if(!token || !usuario) return null

  const usuarioObj = JSON.parse(usuario)

  return (
    <div className="navbar">
      <nav>
        <h1 style={{ cursor: 'pointer', transition: 'all 0.3s ease' }} onClick={() => nav('/controle-acesso')} onMouseEnter={(e) => e.target.style.transform = 'scale(1.05)'} onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}>🔐 Controle de Acesso</h1>
        <ul>
          <li><Link to="/controle-acesso">Monitoramento</Link></li>
          <li><Link to="/acessos-pessoais">Acessos Pessoais</Link></li>
          <li><Link to="/acessos-veiculares">Acessos Veiculares</Link></li>
          <li><Link to="/veiculos">Veículos</Link></li>
          <li><Link to="/empresas">Empresas</Link></li>
          <li><Link to="/usuarios">Usuários</Link></li>
          <li style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{ fontSize: '14px', fontWeight: '500' }}>
              👤 {usuarioObj.nome || usuarioObj.login}
            </span>
            <button 
              onClick={handleLogout}
              style={{
                padding: '8px 16px',
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
                color: '#fff',
                border: '1px solid rgba(255, 255, 255, 0.3)',
                borderRadius: '6px',
                cursor: 'pointer',
                fontSize: '13px',
                fontWeight: '500',
                transition: 'all 0.3s ease'
              }}
              onMouseEnter={(e) => {
                e.target.style.backgroundColor = 'rgba(231, 76, 60, 0.8)';
                e.target.style.borderColor = '#E74C3C';
              }}
              onMouseLeave={(e) => {
                e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.2)';
                e.target.style.borderColor = 'rgba(255, 255, 255, 0.3)';
              }}
            >
              Sair
            </button>
          </li>
        </ul>
      </nav>
    </div>
  )
}

