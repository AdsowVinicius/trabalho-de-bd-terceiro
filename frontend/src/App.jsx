import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Nav from './components/Nav'
import Login from './pages/Login'
import Users from './pages/Users'
import AcessoPessoal from './pages/AcessoPessoal'
import AcessoVeicular from './pages/AcessoVeicular'

export default function App() {
  return (
    <div>
      <Nav />
      <main style={{ padding: 20 }}>
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/usuarios" element={<Users />} />
          <Route path="/acessos-pessoais" element={<AcessoPessoal />} />
          <Route path="/acessos-veiculares" element={<AcessoVeicular />} />
        </Routes>
      </main>
    </div>
  )
}
