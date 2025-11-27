import React from 'react'
import { Link } from 'react-router-dom'

export default function Nav(){
  return (
    <nav style={{ padding: '10px 20px', background:'#222', color:'#fff' }}>
      <Link to="/login" style={{ color:'#fff', marginRight: 12 }}>Login</Link>
      <Link to="/usuarios" style={{ color:'#fff', marginRight: 12 }}>Gestão Usuários</Link>
      <Link to="/acessos-pessoais" style={{ color:'#fff', marginRight: 12 }}>Acessos Pessoais</Link>
      <Link to="/acessos-veiculares" style={{ color:'#fff' }}>Acessos Veiculares</Link>
    </nav>
  )
}
