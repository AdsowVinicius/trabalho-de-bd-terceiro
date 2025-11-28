import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

export default function useAuth() {
  const nav = useNavigate()
  
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      nav('/login', { replace: true })
    }
  }, [nav])
  
  return {
    token: localStorage.getItem('token'),
    usuario: localStorage.getItem('usuario') ? JSON.parse(localStorage.getItem('usuario')) : null
  }
}
