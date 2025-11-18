# Guia de Uso - Sistema de Mapeamento

## Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalar Dependências

```powershell
# Navegar até a pasta de ferramentas
cd "c:\Users\nicol\OneDrive\Avila\0.0 - Portugal\03-Mapeamento-Estabelecimentos\ferramentas"

# Instalar as bibliotecas necessárias
pip install streamlit pandas
```

## Como Usar

### Opção 1: Interface Web (Recomendado)

A interface web oferece uma experiência visual e intuitiva para gerenciar todo o mapeamento.

```powershell
# Executar a interface web
streamlit run interface_web.py
```

Isso abrirá automaticamente uma janela do navegador com o dashboard.

**Funcionalidades disponíveis:**
- 📊 **Dashboard**: Visão geral com métricas e gráficos
- ➕ **Adicionar Estabelecimento**: Formulário completo para cadastro
- 🔍 **Buscar & Filtrar**: Pesquisa avançada nos dados
- 🎯 **Próximos Contatos**: Lista priorizada de prospects
- 📊 **Relatórios**: Análises e exportação de dados

### Opção 2: Uso Programático (Python)

Para automações ou scripts personalizados:

```python
from mapeamento import SistemaMapeamento, Estabelecimento, TipoNegocio

# Inicializar sistema
sistema = SistemaMapeamento()

# Adicionar estabelecimento
novo = Estabelecimento(
    nome="Café da Esquina",
    endereco="Rua do Comercio, 10",
    bairro="Alfama",
    tipo_negocio=TipoNegocio.CAFE.value,
    tem_site=False,
    prioridade_contato=4,
    oportunidades=["Website", "Instagram profissional"]
)

sistema.adicionar_estabelecimento(novo)
sistema.salvar_dados()

# Buscar estabelecimentos
cafes = sistema.buscar_por_tipo("Café")
sem_site = sistema.filtrar_sem_site()
prioritarios = sistema.filtrar_por_prioridade(4)

# Gerar relatório
sistema.gerar_relatorio(bairro="Alfama")

# Exportar para CSV
sistema.exportar_para_csv()
```

## Fluxo de Trabalho Recomendado

### 1. Preparação (Antes de ir ao Bairro)
- Escolher o bairro alvo
- Definir rota de caminhada
- Preparar checklist de observação

### 2. Mapeamento em Campo
Ao visitar cada estabelecimento, observar e anotar:
- ✅ Nome e endereço exato
- ✅ Tipo de negócio
- ✅ Aparência externa (moderno, tradicional, precisa reforma)
- ✅ Movimento de clientes
- ✅ Presença de QR codes, cartazes, etc.
- ✅ URL visível de redes sociais
- ✅ Usar smartphone para verificar presença online

**Dica**: Use um aplicativo de notas no celular ou grave áudios para transcrever depois.

### 3. Cadastro no Sistema
Ao voltar para casa:
- Abrir a interface web
- Cadastrar todos os estabelecimentos mapeados
- Preencher análise de necessidades
- Definir prioridades

### 4. Análise e Priorização
- Usar filtros para identificar oportunidades
- Gerar relatórios por bairro
- Listar próximos contatos prioritários

### 5. Preparação de Abordagem
Para estabelecimentos prioritários:
- Pesquisar mais sobre o negócio online
- Preparar proposta de valor específica
- Definir estratégia de primeiro contato

### 6. Contato e Follow-up
- Marcar estabelecimentos como "Contatado"
- Atualizar status conforme progresso
- Registrar observações das conversas

## Estrutura de Dados

Cada estabelecimento armazena:

```
Informações Básicas:
- Nome, Endereço, Bairro, Tipo de Negócio

Presença Digital:
- Website, Instagram, Facebook, Google Business

Análise Visual:
- Aparência do estabelecimento
- Movimento aparente

Necessidades:
- Precisa site, sistema de gestão, marketing, etc.

Oportunidades:
- Lista de soluções que podem ser oferecidas

Gestão:
- Potencial de cliente (Baixo/Médio/Alto/Muito Alto)
- Prioridade de contato (1-5)
- Status do contato
- Observações gerais
```

## Dicas de Uso

### Para Maximizar Eficiência:
1. **Mapeie em blocos**: Dedique algumas horas para mapear intensivamente um bairro
2. **Seja consistente**: Use sempre os mesmos critérios de avaliação
3. **Seja específico**: Quanto mais detalhes, melhor a análise posterior
4. **Priorize**: Nem todos os estabelecimentos têm o mesmo potencial
5. **Documente bem**: As observações são ouro para a abordagem

### Sinais de Alto Potencial:
- ✅ Estabelecimento movimentado mas sem presença digital
- ✅ Negócio tradicional em área turística
- ✅ Donos jovens e receptivos a inovação
- ✅ Problemas operacionais visíveis (filas, desorganização)
- ✅ Setor com alta competição digital (restaurantes, cafés)

### Red Flags:
- ❌ Estabelecimento muito pequeno ou familiar informal
- ❌ Aparência de estar fechando
- ❌ Já possui sistemas modernos completos
- ❌ Setor com baixa necessidade digital

## Análise por Bairro

### Bairros Recomendados para Começar:

**Alfama** 🏰
- Turístico, muitos restaurantes tradicionais
- Baixa presença digital geralmente
- Alto potencial para sites e sistemas de reserva

**Príncipe Real** 🎨
- Público de alto poder aquisitivo
- Cafés, design shops, boutiques
- Oportunidade para e-commerce e branding

**Campo de Ourique** 🏘️
- Mercado local forte
- Comércio de bairro tradicional
- Potencial para sistemas de gestão e delivery

**Cais do Sodré** 🌊
- Mix de turismo e vida noturna
- Bares e restaurantes modernos
- Concorrência digital alta, precisa destaque

## Exportação e Backup

Os dados são salvos automaticamente em:
```
03-Mapeamento-Estabelecimentos/dados/estabelecimentos.json
```

Para backup:
- Copie o arquivo JSON regularmente
- Use o botão "Exportar para CSV" na interface
- Considere usar Git para versionamento

## Próximos Passos

1. Escolha o primeiro bairro para mapear
2. Dedique um dia para o mapeamento em campo
3. Cadastre todos os dados no sistema
4. Analise os resultados e defina top 10 prioridades
5. Prepare materiais de abordagem
6. Inicie os contatos!

---

**Boa sorte com o mapeamento! 🚀**
