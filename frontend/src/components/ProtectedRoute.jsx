import React from 'react'
import { Navigate } from 'react-router-dom'

export default function ProtectedRoute({ element }) {
  const token = localStorage.getItem('token')
  
  // Se não tem token, redireciona para login
  if (!token) {
    return <Navigate to="/login" replace />
  }
  
  // Se tem token, renderiza o componente
  return element
}
