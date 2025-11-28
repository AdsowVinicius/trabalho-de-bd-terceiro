const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8001'

async function request(path, options = {}) {
  const res = await fetch(BASE + path, options)
  const text = await res.text()
  try { return { status: res.status, data: text ? JSON.parse(text) : null } }
  catch { return { status: res.status, data: text } }
}

export async function fetchLookups(){
  // Try a set of endpoints; backend may not implement all, so fallback to empty arrays
  const lookups = {}
  const endpoints = {
    perfis: '/lookups/perfis',
    tiposUsuario: '/lookups/tipos-usuario',
    tiposEmpresa: '/lookups/tipos-empresa',
    tiposServico: '/lookups/tipos-servico',
    empresas: '/lookups/empresas',
    veiculos: '/lookups/veiculos',
    responsaveis: '/lookups/responsaveis',
    transportadoras: '/lookups/transportadoras'
  }
  for(const [k, ep] of Object.entries(endpoints)){
    try{
      const r = await request(ep)
      lookups[k] = (r.status === 200 && Array.isArray(r.data)) ? r.data : []
    }catch(e){ lookups[k] = [] }
  }
  return lookups
}

export async function login(payload){
  return request('/usuarios/login', {
    method: 'POST',
    headers: { 'Content-Type':'application/json' },
    body: JSON.stringify(payload)
  })
}

export async function registerUser(payload, token){
  return request('/usuarios/registro', {
    method: 'POST',
    headers: { 'Content-Type':'application/json', ...(token?{Authorization: 'Bearer '+token}: {}) },
    body: JSON.stringify(payload)
  })
}

export async function createVeiculo(payload, token){
  return request('/veiculos/', {
    method: 'POST', headers: { 'Content-Type':'application/json', Authorization: 'Bearer '+token }, body: JSON.stringify(payload)
  })
}

export async function createAcessoPessoal(payload, token){
  return request('/acessos-pessoais/', {
    method: 'POST', headers: { 'Content-Type':'application/json', Authorization: 'Bearer '+token }, body: JSON.stringify(payload)
  })
}

export async function createAcessoVeicular(payload, token){
  return request('/acessos-veiculares/', {
    method: 'POST', headers: { 'Content-Type':'application/json', Authorization: 'Bearer '+token }, body: JSON.stringify(payload)
  })
}

export async function listUsers(){
  return request('/usuarios/')
}

export async function getAcessosPessoaisAtivos(token){
  return request('/acessos-pessoais/', {
    headers: { ...(token?{Authorization: 'Bearer '+token}: {}) }
  })
}

export async function getAcessosVeiculaesAtivos(token){
  return request('/acessos-veiculares/', {
    headers: { ...(token?{Authorization: 'Bearer '+token}: {}) }
  })
}

export async function darSaidaPessoal(acessoId, token){
  return request(`/acessos-pessoais/${acessoId}/saida`, {
    method: 'PUT',
    headers: { 'Content-Type':'application/json', Authorization: 'Bearer '+token },
    body: JSON.stringify({})
  })
}

export async function darSaidaVeicular(acessoId, token){
  return request(`/acessos-veiculares/${acessoId}/saida`, {
    method: 'PUT',
    headers: { 'Content-Type':'application/json', Authorization: 'Bearer '+token },
    body: JSON.stringify({})
  })
}

export async function updateUser(usuarioId, payload, token){
  return request(`/usuarios/${usuarioId}`, {
    method: 'PUT',
    headers: { 'Content-Type':'application/json', Authorization: 'Bearer '+token },
    body: JSON.stringify(payload)
  })
}

export async function deleteUser(usuarioId, token){
  return request(`/usuarios/${usuarioId}`, {
    method: 'DELETE',
    headers: { Authorization: 'Bearer '+token }
  })
}

export default { fetchLookups, login, registerUser, createVeiculo, createAcessoPessoal, createAcessoVeicular, listUsers, getAcessosPessoaisAtivos, getAcessosVeiculaesAtivos, darSaidaPessoal, darSaidaVeicular, updateUser, deleteUser }
