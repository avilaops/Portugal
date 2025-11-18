# 🔐 Sistema de Autenticação - Ávila Portugal

## Credenciais de Teste

Enquanto o backend `auth.avila.inc` não estiver implementado, use estas credenciais temporárias:

### Usuários Disponíveis

| E-mail | Senha | Perfil |
|--------|-------|--------|
| `nicolas@avila.inc` | `avila2025` | Administrador |
| `admin@avila.inc` | `admin123` | Administrador |
| `portugal@avila.inc` | `lisboa2025` | Usuário |

## Fluxo de Autenticação

1. **Login** → `login.html`
   - Tenta autenticar via `auth.avila.inc/api/v1/auth/login`
   - Se a API não responder, usa autenticação local (fallback)
   - Salva token e informações do usuário no localStorage

2. **Proteção de Páginas**
   - `mapeamento.html` verifica se existe `avila_auth_token`
   - Redireciona para login se não autenticado
   - Mostra informações do usuário no header

3. **Logout**
   - Remove token e dados do usuário
   - Redireciona para login

## Integração com APIs

### auth.avila.inc
```javascript
POST https://auth.avila.inc/api/v1/auth/login
Content-Type: application/json

{
  "email": "usuario@avila.inc",
  "password": "senha123"
}
```

**Resposta esperada:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "usuario@avila.inc",
    "name": "Nome do Usuário",
    "role": "admin"
  }
}
```

### api.avila.inc

O módulo `js/avila-api.js` fornece integração completa com a API:

```javascript
// Listar estabelecimentos
const data = await avilaAPI.getEstabelecimentos();

// Criar estabelecimento
await avilaAPI.createEstabelecimento({
  nome: "Restaurante Exemplo",
  tipo: "Restaurante",
  bairro: "Alfama"
});

// Dashboard stats
const stats = await avilaAPI.getDashboardStats();

// Sincronizar dados
await avilaAPI.syncData(localData);

// Analytics
await avilaAPI.trackEvent('pagina_visitada', { page: 'dashboard' });
```

### portal.avila.inc

Links integrados para:
- Gestão completa de projetos
- Relatórios avançados
- Configurações da conta

## Sistema Híbrido

O sistema funciona em modo híbrido:

✅ **Online**: Dados salvos localmente + sincronizados com `api.avila.inc`
✅ **Offline**: Continua funcionando com localStorage
✅ **Automático**: Sincronização automática ao recuperar conexão

## Estrutura de Arquivos

```
docs/
├── login.html           # Página de login
├── mapeamento.html      # Sistema principal (protegido)
├── index.html           # Landing page pública
└── js/
    ├── avila-api.js     # Cliente API api.avila.inc
    └── github-sync.js   # Sincronização GitHub
```

## Implementação Backend (TODO)

Para produção, implementar:

1. **auth.avila.inc**
   - `POST /api/v1/auth/login` - Login
   - `POST /api/v1/auth/register` - Registro
   - `POST /api/v1/auth/refresh` - Refresh token
   - `POST /api/v1/auth/logout` - Logout

2. **api.avila.inc**
   - CRUD de estabelecimentos
   - Dashboard e estatísticas
   - Sistema de sincronização
   - Analytics e relatórios

## Segurança

⚠️ **IMPORTANTE**: As credenciais hardcoded são APENAS para desenvolvimento!

Em produção:
- Remover credenciais do código
- Implementar backend real
- Usar HTTPS em todas as APIs
- Implementar rate limiting
- Adicionar 2FA (opcional)
- Validar tokens com JWT
