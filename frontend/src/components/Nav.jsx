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
    <nav style={{ padding: '10px 20px', background:'#222', color:'#fff', display:'flex', justifyContent:'space-between', alignItems:'center' }}>
      <div>
        <Link to="/controle-acesso" style={{ color:'#fff', marginRight: 12, fontWeight:'bold' }}>Controle de Acesso</Link>
        <Link to="/acessos-pessoais" style={{ color:'#fff', marginRight: 12 }}>Acessos Pessoais</Link>
        <Link to="/acessos-veiculares" style={{ color:'#fff', marginRight: 12 }}>Acessos Veiculares</Link>
        <Link to="/veiculos" style={{ color:'#fff', marginRight: 12 }}>Gestão Veículos</Link>
        <Link to="/empresas" style={{ color:'#fff', marginRight: 12 }}>Gestão Empresas</Link>
        <Link to="/usuarios" style={{ color:'#fff', marginRight: 12 }}>Gestão Usuários</Link>
      </div>
      <div style={{ display:'flex', alignItems:'center', gap:'15px' }}>
        <span style={{ fontSize:'14px' }}>Olá, {usuarioObj.nome || usuarioObj.login}</span>
        <button 
          onClick={handleLogout}
          style={{ padding:'8px 16px', backgroundColor:'#f44336', color:'#fff', border:'none', borderRadius:'4px', cursor:'pointer' }}
        >
          Logout
        </button>
      </div>
    </nav>
  )
}

