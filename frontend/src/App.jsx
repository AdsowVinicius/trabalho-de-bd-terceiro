import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Nav from './components/Nav'
import ProtectedRoute from './components/ProtectedRoute'
import Login from './pages/Login'
import Users from './pages/Users'
import AcessoPessoal from './pages/AcessoPessoal'
import AcessoVeicular from './pages/AcessoVeicular'
import ControleAcesso from './pages/ControleAcesso'
import Veiculos from './pages/Veiculos'
import Empresas from './pages/Empresas'

export default function App() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Nav />
      <main style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<Navigate to="/controle-acesso" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/usuarios" element={<ProtectedRoute element={<Users />} />} />
          <Route path="/veiculos" element={<ProtectedRoute element={<Veiculos />} />} />
          <Route path="/empresas" element={<ProtectedRoute element={<Empresas />} />} />
          <Route path="/acessos-pessoais" element={<ProtectedRoute element={<AcessoPessoal />} />} />
          <Route path="/acessos-veiculares" element={<ProtectedRoute element={<AcessoVeicular />} />} />
          <Route path="/controle-acesso" element={<ProtectedRoute element={<ControleAcesso />} />} />
        </Routes>
      </main>
    </div>
  )
}

