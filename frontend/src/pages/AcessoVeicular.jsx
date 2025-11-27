import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'
import FormField from '../components/FormField'

export default function AcessoVeicular(){
  const [form, setForm] = useState({ 
    id_veiculo:'', 
    placa:'',
    ano:'',
    modelo:'',
    id_responsavel:'', 
    id_tipo_servico:1, 
    nota_fiscal_entrada:'', 
    nota_fiscal_saida:'',
    id_transportadora:null,
    observacao:'' 
  })
  const [lookups, setLookups] = useState({ 
    tiposServico:[], 
    veiculos:[],
    responsaveis:[],
    transportadoras:[]
  })
  const [veiculosFiltrados, setVeiculosFiltrados] = useState([])
  const [responsaveisFiltrados, setResponsaveisFiltrados] = useState([])
  const [transportadorasFiltradas, setTransportadorasFiltradas] = useState([])
  
  const [veiculoSelecionado, setVeiculoSelecionado] = useState(null)
  const [responsavelSelecionado, setResponsavelSelecionado] = useState(null)
  const [transportadoraSelecionada, setTransportadoraSelecionada] = useState(null)
  
  const [showVeiculosList, setShowVeiculosList] = useState(false)
  const [showResponsaveisList, setShowResponsaveisList] = useState(false)
  const [showTransportadorasList, setShowTransportadorasList] = useState(false)
  
  const [searchVeiculo, setSearchVeiculo] = useState('')
  const [searchResponsavel, setSearchResponsavel] = useState('')
  const [searchTransportadora, setSearchTransportadora] = useState('')
  
  const [showNovoVeiculo, setShowNovoVeiculo] = useState(false)
  const [showNovoResponsavel, setShowNovoResponsavel] = useState(false)
  const [showNovaTransportadora, setShowNovaTransportadora] = useState(false)
  
  const token = localStorage.getItem('token')
  const nav = useNavigate()

  useEffect(()=>{
    api.fetchLookups().then(l=> setLookups({ 
      tiposServico: l.tiposServico||[], 
      veiculos: l.veiculos||[],
      responsaveis: l.responsaveis||[],
      transportadoras: l.transportadoras||[]
    }))
  },[])

  // Filtrar veículos por placa ou modelo
  const handleSearchVeiculo = (valor) => {
    setSearchVeiculo(valor)
    if(valor.trim()){
      const filtrados = (lookups.veiculos||[]).filter(v=>
        v.placa.toLowerCase().includes(valor.toLowerCase()) ||
        (v.modelo && v.modelo.toLowerCase().includes(valor.toLowerCase()))
      )
      setVeiculosFiltrados(filtrados)
      setShowVeiculosList(true)
    } else {
      setVeiculosFiltrados([])
      setShowVeiculosList(false)
    }
  }

  // Filtrar responsáveis por nome ou documento
  const handleSearchResponsavel = (valor) => {
    setSearchResponsavel(valor)
    if(valor.trim()){
      const filtrados = (lookups.responsaveis||[]).filter(r=>
        r.nome.toLowerCase().includes(valor.toLowerCase()) ||
        r.documento.includes(valor) ||
        r.login.toLowerCase().includes(valor.toLowerCase())
      )
      setResponsaveisFiltrados(filtrados)
      setShowResponsaveisList(true)
    } else {
      setResponsaveisFiltrados([])
      setShowResponsaveisList(false)
    }
  }

  // Filtrar transportadoras por nome
  const handleSearchTransportadora = (valor) => {
    setSearchTransportadora(valor)
    if(valor.trim()){
      const filtradas = (lookups.transportadoras||[]).filter(t=>
        t.nome.toLowerCase().includes(valor.toLowerCase())
      )
      setTransportadorasFiltradas(filtradas)
      setShowTransportadorasList(true)
    } else {
      setTransportadorasFiltradas([])
      setShowTransportadorasList(false)
    }
  }

  // Selecionar veículo
  const selecionarVeiculo = (veiculo) => {
    setVeiculoSelecionado(veiculo)
    setForm({
      ...form, 
      id_veiculo: veiculo.id, 
      placa: veiculo.placa,
      ano: veiculo.ano,
      modelo: veiculo.modelo
    })
    setSearchVeiculo(`${veiculo.placa} (${veiculo.modelo || 'N/A'}) - ${veiculo.ano || 'N/A'}`)
    setShowVeiculosList(false)
  }

  // Selecionar responsável
  const selecionarResponsavel = (responsavel) => {
    setResponsavelSelecionado(responsavel)
    setForm({...form, id_responsavel: responsavel.id})
    setSearchResponsavel(`${responsavel.nome} (${responsavel.documento})`)
    setShowResponsaveisList(false)
  }

  // Selecionar transportadora
  const selecionarTransportadora = (transportadora) => {
    setTransportadoraSelecionada(transportadora)
    setForm({...form, id_transportadora: transportadora.id})
    setSearchTransportadora(transportadora.nome)
    setShowTransportadorasList(false)
  }

  async function submit(e){
    e.preventDefault()
    if(!veiculoSelecionado){
      alert('Por favor, selecione um veiculo')
      return
    }
    if(!responsavelSelecionado){
      alert('Por favor, selecione um responsavel')
      return
    }
    const r = await api.createAcessoVeicular(form, token)
    if(r.status===201){ 
      alert('Acesso veicular registrado com sucesso')
      setForm({ 
        id_veiculo:'', 
        placa:'',
        ano:'',
        modelo:'',
        id_responsavel:'', 
        id_tipo_servico:1, 
        nota_fiscal_entrada:'', 
        nota_fiscal_saida:'',
        id_transportadora:null,
        observacao:'' 
      })
      setVeiculoSelecionado(null)
      setResponsavelSelecionado(null)
      setTransportadoraSelecionada(null)
      setSearchVeiculo('')
      setSearchResponsavel('')
      setSearchTransportadora('')
    }
    else alert('Erro: '+(r.data?.detail||JSON.stringify(r.data)))
  }

  return (
    <div style={{ maxWidth:900, margin:'20px auto' }}>
      <h2>Registrar Acesso Veicular</h2>
      
      <form onSubmit={submit}>
        {/* Campo de Veículo com Busca */}
        <FormField label="Pesquisar Veiculo">
          <div style={{ position:'relative' }}>
            <input 
              type="text"
              placeholder="Digite placa ou modelo do veiculo"
              value={searchVeiculo}
              onChange={e=>handleSearchVeiculo(e.target.value)}
              onFocus={()=>searchVeiculo.trim() && setShowVeiculosList(true)}
            />
            {showVeiculosList && (
              <div style={{ 
                position:'absolute', 
                top:'100%', 
                left:0, 
                right:0, 
                border:'1px solid #ddd', 
                maxHeight:'200px', 
                overflowY:'auto',
                backgroundColor:'white',
                zIndex:10
              }}>
                {veiculosFiltrados.length > 0 ? (
                  veiculosFiltrados.map(v=>
                    <div 
                      key={v.id}
                      onClick={()=>selecionarVeiculo(v)}
                      style={{ padding:'8px', borderBottom:'1px solid #eee', cursor:'pointer', backgroundColor: veiculoSelecionado?.id===v.id?'#e3f2fd':'white' }}
                    >
                      <strong>{v.placa}</strong> - {v.modelo || 'Modelo N/A'} ({v.ano || 'Ano N/A'})
                    </div>
                  )
                ) : (
                  <div style={{ padding:'8px', color:'#999' }}>Nenhum veiculo encontrado</div>
                )}
              </div>
            )}
          </div>
          {veiculoSelecionado && (
            <button type="button" onClick={()=>{setVeiculoSelecionado(null); setSearchVeiculo(''); setForm({...form, id_veiculo:'', placa:'', ano:'', modelo:''})}} style={{ marginTop:'8px' }}>
              Limpar Selecao
            </button>
          )}
        </FormField>

        {/* Dados do Veiculo (apenas leitura) */}
        {veiculoSelecionado && (
          <>
            <FormField label="Placa">
              <input type="text" value={form.placa} disabled />
            </FormField>
            <FormField label="Ano">
              <input type="text" value={form.ano} disabled />
            </FormField>
            <FormField label="Modelo">
              <input type="text" value={form.modelo} disabled />
            </FormField>
          </>
        )}

        {/* Campo de Responsável com Busca */}
        <FormField label="Pesquisar Responsavel (Motorista)">
          <div style={{ position:'relative' }}>
            <input 
              type="text"
              placeholder="Digite nome, documento ou login do responsavel"
              value={searchResponsavel}
              onChange={e=>handleSearchResponsavel(e.target.value)}
              onFocus={()=>searchResponsavel.trim() && setShowResponsaveisList(true)}
            />
            {showResponsaveisList && (
              <div style={{ 
                position:'absolute', 
                top:'100%', 
                left:0, 
                right:0, 
                border:'1px solid #ddd', 
                maxHeight:'200px', 
                overflowY:'auto',
                backgroundColor:'white',
                zIndex:10
              }}>
                {responsaveisFiltrados.length > 0 ? (
                  responsaveisFiltrados.map(r=>
                    <div 
                      key={r.id}
                      onClick={()=>selecionarResponsavel(r)}
                      style={{ padding:'8px', borderBottom:'1px solid #eee', cursor:'pointer', backgroundColor: responsavelSelecionado?.id===r.id?'#e3f2fd':'white' }}
                    >
                      <strong>{r.nome}</strong> ({r.documento}) - {r.login}
                    </div>
                  )
                ) : (
                  <div style={{ padding:'8px', color:'#999' }}>Nenhum responsavel encontrado</div>
                )}
              </div>
            )}
          </div>
          {responsavelSelecionado && (
            <button type="button" onClick={()=>{setResponsavelSelecionado(null); setSearchResponsavel(''); setForm({...form, id_responsavel:''})}} style={{ marginTop:'8px' }}>
              Limpar Selecao
            </button>
          )}
        </FormField>

        {/* Tipo de Serviço */}
        <FormField label="Tipo de Servico">
          <select value={form.id_tipo_servico} onChange={e=>setForm({...form,id_tipo_servico:parseInt(e.target.value)})}>
            {(lookups.tiposServico||[]).length ? lookups.tiposServico.map(t=> <option key={t.id} value={t.id}>{t.nome}</option>) : <option value={1}>Padrao</option> }
          </select>
        </FormField>

        {/* Nota Fiscal Entrada */}
        <FormField label="Nota Fiscal Entrada">
          <input 
            type="text"
            value={form.nota_fiscal_entrada} 
            onChange={e=>setForm({...form,nota_fiscal_entrada:e.target.value})}
            placeholder="Ex: NF-001234"
          />
        </FormField>

        {/* Nota Fiscal Saída */}
        <FormField label="Nota Fiscal Saida">
          <input 
            type="text"
            value={form.nota_fiscal_saida} 
            onChange={e=>setForm({...form,nota_fiscal_saida:e.target.value})}
            placeholder="Ex: NF-001235"
          />
        </FormField>

        {/* Campo de Transportadora com Busca */}
        <FormField label="Pesquisar Transportadora (Opcional)">
          <div style={{ position:'relative' }}>
            <input 
              type="text"
              placeholder="Digite nome da transportadora"
              value={searchTransportadora}
              onChange={e=>handleSearchTransportadora(e.target.value)}
              onFocus={()=>searchTransportadora.trim() && setShowTransportadorasList(true)}
            />
            {showTransportadorasList && (
              <div style={{ 
                position:'absolute', 
                top:'100%', 
                left:0, 
                right:0, 
                border:'1px solid #ddd', 
                maxHeight:'200px', 
                overflowY:'auto',
                backgroundColor:'white',
                zIndex:10
              }}>
                {transportadorasFiltradas.length > 0 ? (
                  transportadorasFiltradas.map(t=>
                    <div 
                      key={t.id}
                      onClick={()=>selecionarTransportadora(t)}
                      style={{ padding:'8px', borderBottom:'1px solid #eee', cursor:'pointer', backgroundColor: transportadoraSelecionada?.id===t.id?'#e3f2fd':'white' }}
                    >
                      <strong>{t.nome}</strong> {t.cnpj && `(${t.cnpj})`}
                    </div>
                  )
                ) : (
                  <div style={{ padding:'8px', color:'#999' }}>Nenhuma transportadora encontrada</div>
                )}
              </div>
            )}
          </div>
          {transportadoraSelecionada && (
            <button type="button" onClick={()=>{setTransportadoraSelecionada(null); setSearchTransportadora(''); setForm({...form, id_transportadora:null})}} style={{ marginTop:'8px' }}>
              Limpar Selecao
            </button>
          )}
        </FormField>

        {/* Observação */}
        <FormField label="Observacao">
          <textarea 
            value={form.observacao} 
            onChange={e=>setForm({...form,observacao:e.target.value})}
            placeholder="Informacoes adicionais sobre o acesso"
            rows={4}
          />
        </FormField>

        {/* Botões de Ação */}
        <div style={{ display:'flex', gap:'10px', marginTop:'20px', flexWrap:'wrap' }}>
          <button type="submit" disabled={!veiculoSelecionado || !responsavelSelecionado} style={{ flex:1, minWidth:'150px' }}>
            Registrar Acesso Veicular
          </button>
          <button 
            type="button" 
            onClick={()=>setShowNovoVeiculo(!showNovoVeiculo)}
            style={{ flex:1, minWidth:'150px', backgroundColor:'#ff9800' }}
          >
            {showNovoVeiculo ? 'Cancelar' : 'Cadastrar Novo Veiculo'}
          </button>
          <button 
            type="button" 
            onClick={()=>setShowNovoResponsavel(!showNovoResponsavel)}
            style={{ flex:1, minWidth:'150px', backgroundColor:'#ff9800' }}
          >
            {showNovoResponsavel ? 'Cancelar' : 'Cadastrar Novo Responsavel'}
          </button>
          <button 
            type="button" 
            onClick={()=>setShowNovaTransportadora(!showNovaTransportadora)}
            style={{ flex:1, minWidth:'150px', backgroundColor:'#ff9800' }}
          >
            {showNovaTransportadora ? 'Cancelar' : 'Cadastrar Nova Transportadora'}
          </button>
        </div>
      </form>

      {/* Modal Novo Veiculo */}
      {showNovoVeiculo && (
        <div style={{ marginTop:'30px', border:'2px solid #ff9800', padding:'20px', borderRadius:'8px', backgroundColor:'#fff3e0' }}>
          <h3>Cadastrar Novo Veiculo</h3>
          <p style={{ color:'#666' }}>Ir para pagina de Gestao de Veiculos para adicionar um novo veiculo</p>
          <button 
            type="button"
            onClick={()=>nav('/users')}  // TODO: change to /veiculos when page created
            style={{ width:'100%', padding:'12px', backgroundColor:'#4CAF50', color:'white', border:'none', borderRadius:'4px', cursor:'pointer', fontSize:'16px' }}
          >
            Ir para Gestao de Veiculos
          </button>
        </div>
      )}

      {/* Modal Novo Responsável */}
      {showNovoResponsavel && (
        <div style={{ marginTop:'30px', border:'2px solid #ff9800', padding:'20px', borderRadius:'8px', backgroundColor:'#fff3e0' }}>
          <h3>Cadastrar Novo Responsavel</h3>
          <p style={{ color:'#666' }}>Ir para pagina de Gestao de Usuarios para adicionar um novo motorista/condutor</p>
          <button 
            type="button"
            onClick={()=>nav('/users')}
            style={{ width:'100%', padding:'12px', backgroundColor:'#4CAF50', color:'white', border:'none', borderRadius:'4px', cursor:'pointer', fontSize:'16px' }}
          >
            Ir para Gestao de Usuarios
          </button>
        </div>
      )}

      {/* Modal Nova Transportadora */}
      {showNovaTransportadora && (
        <div style={{ marginTop:'30px', border:'2px solid #ff9800', padding:'20px', borderRadius:'8px', backgroundColor:'#fff3e0' }}>
          <h3>Cadastrar Nova Transportadora</h3>
          <p style={{ color:'#666' }}>Ir para pagina de Gestao de Empresas para adicionar uma nova transportadora</p>
          <button 
            type="button"
            onClick={()=>nav('/users')}  // TODO: change to /empresas when page created
            style={{ width:'100%', padding:'12px', backgroundColor:'#4CAF50', color:'white', border:'none', borderRadius:'4px', cursor:'pointer', fontSize:'16px' }}
          >
            Ir para Gestao de Empresas
          </button>
        </div>
      )}
    </div>
  )
}
