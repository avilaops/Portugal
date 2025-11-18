# Configuração do GitHub Pages

## Estrutura criada:

```
docs/
├── index.html          # Página principal do projeto
└── mapeamento.html     # Sistema de mapeamento web
```

## Configurar no GitHub:

1. **Fazer commit e push:**
```powershell
cd "c:\Users\nicol\OneDrive\Avila\0.0 - Portugal"
git add .
git commit -m "Add website - portugal.avila.inc"
git push origin main
```

2. **Configurar GitHub Pages:**
   - Ir em: https://github.com/avilaops/Portural/settings/pages
   - Em "Source", selecionar: **main** branch
   - Em "Folder", selecionar: **/docs**
   - Clicar em **Save**

3. **O site ficará disponível em:**
   - https://avilaops.github.io/Portural/
   - https://portugal.avila.inc (já configurado no Cloudflare)

## Cloudflare

Como você já configurou o Cloudflare para apontar para o GitHub Pages:
- O DNS deve estar apontando para: `avilaops.github.io`
- CNAME configurado: `portugal.avila.inc` → `avilaops.github.io`

## Adicionar CNAME (para domínio customizado):

Crie o arquivo:
```
docs/CNAME
```

Com o conteúdo:
```
portugal.avila.inc
```

## Features do Site:

### Página Principal (index.html):
- ✅ Visão geral do projeto
- ✅ 3 frentes principais (Visto, Abertura, Mapeamento)
- ✅ Timeline do projeto
- ✅ Bairros prioritários
- ✅ Soluções oferecidas
- ✅ Design responsivo e moderno

### Sistema de Mapeamento (mapeamento.html):
- ✅ Dashboard com métricas
- ✅ Formulário de cadastro
- ✅ Lista de todos os estabelecimentos
- ✅ Priorização automática de contatos
- ✅ Armazenamento local (localStorage)
- ✅ Interface totalmente funcional

## Verificar depois do deploy:

1. Site principal: https://portugal.avila.inc
2. Sistema de mapeamento: https://portugal.avila.inc/mapeamento.html
3. GitHub Pages: https://avilaops.github.io/Portural/

## Próximos passos opcionais:

- Adicionar Google Analytics
- Adicionar formulário de contato
- Conectar com backend real (API)
- Adicionar autenticação para o sistema de mapeamento
