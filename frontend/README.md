# Frontend - Controle de Acesso

Pequeno frontend React (Vite) para consumir a API de Controle de Acesso.

Pré-requisitos:
- Node.js (v18+ recomendado)
- Yarn ou npm

Como instalar e rodar:

```bash
cd frontend
npm install
npm run dev
```

O frontend usa a variável `VITE_API_URL` (opcional) para apontar para sua API. Por padrão assume `http://localhost:8001`.

Importante:
- A página de login aceita apenas usuários com perfil nomeado `Porteiro`. Se o seu banco usa outro nome, ajuste o texto no `src/pages/Login.jsx`.
- As opções de lookup (perfis, tipos) são buscadas de endpoints `GET /lookups/*`. Se seu backend não expõe esses endpoints, o frontend tentará usar valores padrão.

Páginas:
- `/login` - login para porteiros
- `/usuarios` - gestão de usuários (criar/listar)
- `/acessos-pessoais` - formulário de registro de entrada pessoal
- `/acessos-veiculares` - formulário de registro de entrada veicular

Se quiser, eu posso gerar uma coleção Insomnia/Postman a partir dessas rotas.
