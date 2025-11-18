"""
Interface Web para Sistema de Mapeamento
Dashboard interativo usando Streamlit
"""

try:
    import streamlit as st
except ImportError:
    print("⚠️  Streamlit não instalado. Execute: pip install streamlit")
    exit(1)

import pandas as pd
from mapeamento import (
    SistemaMapeamento,
    Estabelecimento,
    TipoNegocio,
    NivelPresencaDigital,
    PotencialCliente,
)
from dataclasses import asdict

# Configuração da página
st.set_page_config(page_title="Mapeamento Lisboa - Ávila", page_icon="🗺️", layout="wide")


# Inicializar sistema
@st.cache_resource
def get_sistema():
    return SistemaMapeamento()


sistema = get_sistema()

# Sidebar - Menu
st.sidebar.title("🗺️ Mapeamento Lisboa")
menu = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Adicionar Estabelecimento",
        "Buscar & Filtrar",
        "Próximos Contatos",
        "Relatórios",
    ],
)

# DASHBOARD
if menu == "Dashboard":
    st.title("📊 Dashboard - Mapeamento de Estabelecimentos")

    if not sistema.estabelecimentos:
        st.warning("Nenhum estabelecimento mapeado ainda. Comece adicionando alguns!")
    else:
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Mapeados", len(sistema.estabelecimentos))

        with col2:
            sem_site = len([e for e in sistema.estabelecimentos if not e.tem_site])
            st.metric("Sem Website", sem_site)

        with col3:
            alta_prioridade = len(
                [e for e in sistema.estabelecimentos if e.prioridade_contato >= 4]
            )
            st.metric("Alta Prioridade", alta_prioridade)

        with col4:
            nao_contatados = len(
                [
                    e
                    for e in sistema.estabelecimentos
                    if e.status_contato == "Não contatado"
                ]
            )
            st.metric("Não Contatados", nao_contatados)

        # Gráficos
        st.subheader("📈 Análises")

        col1, col2 = st.columns(2)

        with col1:
            # Distribuição por tipo de negócio
            df = pd.DataFrame([asdict(e) for e in sistema.estabelecimentos])
            tipo_counts = df["tipo_negocio"].value_counts()
            st.bar_chart(tipo_counts)
            st.caption("Distribuição por Tipo de Negócio")

        with col2:
            # Distribuição por bairro
            bairro_counts = df["bairro"].value_counts()
            st.bar_chart(bairro_counts)
            st.caption("Distribuição por Bairro")

# ADICIONAR ESTABELECIMENTO
elif menu == "Adicionar Estabelecimento":
    st.title("➕ Adicionar Novo Estabelecimento")

    with st.form("novo_estabelecimento"):
        st.subheader("Informações Básicas")
        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input(
                "Nome do Estabelecimento*", placeholder="Ex: Café Central"
            )
            endereco = st.text_input("Endereço*", placeholder="Ex: Rua Augusta, 123")
            bairro = st.text_input("Bairro*", placeholder="Ex: Chiado")

        with col2:
            tipo_negocio = st.selectbox(
                "Tipo de Negócio*", [t.value for t in TipoNegocio]
            )
            aparencia = st.text_input(
                "Aparência", placeholder="Ex: Moderno, Tradicional"
            )
            movimento = st.selectbox(
                "Movimento Aparente", ["", "Baixo", "Médio", "Alto"]
            )

        st.subheader("Presença Digital")
        col1, col2, col3 = st.columns(3)

        with col1:
            tem_site = st.checkbox("Tem Website?")
            url_site = (
                st.text_input("URL do Site", placeholder="https://...")
                if tem_site
                else ""
            )

        with col2:
            tem_instagram = st.checkbox("Tem Instagram?")
            url_instagram = (
                st.text_input("Instagram", placeholder="@usuario")
                if tem_instagram
                else ""
            )

        with col3:
            tem_facebook = st.checkbox("Tem Facebook?")
            tem_google_business = st.checkbox("Tem Google Business?")

        nivel_digital = st.selectbox(
            "Nível de Presença Digital", [n.value for n in NivelPresencaDigital]
        )

        st.subheader("Necessidades Identificadas")
        col1, col2 = st.columns(2)

        with col1:
            precisa_site = st.checkbox("Precisa Website")
            precisa_sistema_gestao = st.checkbox("Precisa Sistema de Gestão")
            precisa_marketing = st.checkbox("Precisa Marketing Digital")

        with col2:
            precisa_reservas = st.checkbox("Precisa Sistema de Reservas")
            precisa_ecommerce = st.checkbox("Precisa E-commerce")

        st.subheader("Oportunidades e Análise")
        oportunidades_text = st.text_area(
            "Oportunidades (uma por linha)",
            placeholder="Website profissional\nSistema de reservas online\nMarketing nas redes sociais",
        )
        oportunidades = [o.strip() for o in oportunidades_text.split("\n") if o.strip()]

        observacoes = st.text_area(
            "Observações", placeholder="Detalhes adicionais sobre o estabelecimento..."
        )

        col1, col2 = st.columns(2)
        with col1:
            potencial = st.selectbox(
                "Potencial de Cliente", [p.value for p in PotencialCliente]
            )
        with col2:
            prioridade = st.slider("Prioridade de Contato", 1, 5, 3)

        submitted = st.form_submit_button("💾 Salvar Estabelecimento")

        if submitted:
            if not nome or not endereco or not bairro:
                st.error("Por favor, preencha todos os campos obrigatórios (*)!")
            else:
                novo = Estabelecimento(
                    nome=nome,
                    endereco=endereco,
                    bairro=bairro,
                    tipo_negocio=tipo_negocio,
                    tem_site=tem_site,
                    url_site=url_site if tem_site else None,
                    tem_instagram=tem_instagram,
                    url_instagram=url_instagram if tem_instagram else None,
                    tem_facebook=tem_facebook,
                    tem_google_business=tem_google_business,
                    aparencia_estabelecimento=aparencia or None,
                    movimento_aparente=movimento or None,
                    nivel_presenca_digital=nivel_digital,
                    precisa_site=precisa_site,
                    precisa_sistema_gestao=precisa_sistema_gestao,
                    precisa_marketing_digital=precisa_marketing,
                    precisa_sistema_reservas=precisa_reservas,
                    precisa_ecommerce=precisa_ecommerce,
                    oportunidades=oportunidades,
                    observacoes=observacoes,
                    potencial_cliente=potencial,
                    prioridade_contato=prioridade,
                )

                sistema.adicionar_estabelecimento(novo)
                sistema.salvar_dados()
                st.success(f"✅ '{nome}' adicionado com sucesso!")
                st.balloons()

# BUSCAR & FILTRAR
elif menu == "Buscar & Filtrar":
    st.title("🔍 Buscar & Filtrar Estabelecimentos")

    if not sistema.estabelecimentos:
        st.warning("Nenhum estabelecimento mapeado ainda.")
    else:
        # Filtros
        col1, col2, col3 = st.columns(3)

        with col1:
            busca_nome = st.text_input(
                "Buscar por Nome", placeholder="Digite o nome..."
            )

        with col2:
            bairros = ["Todos"] + sorted(
                list(set(e.bairro for e in sistema.estabelecimentos))
            )
            filtro_bairro = st.selectbox("Filtrar por Bairro", bairros)

        with col3:
            tipos = ["Todos"] + sorted(
                list(set(e.tipo_negocio for e in sistema.estabelecimentos))
            )
            filtro_tipo = st.selectbox("Filtrar por Tipo", tipos)

        # Aplicar filtros
        resultados = sistema.estabelecimentos

        if busca_nome:
            resultados = [e for e in resultados if busca_nome.lower() in e.nome.lower()]

        if filtro_bairro != "Todos":
            resultados = [e for e in resultados if e.bairro == filtro_bairro]

        if filtro_tipo != "Todos":
            resultados = [e for e in resultados if e.tipo_negocio == filtro_tipo]

        # Mostrar resultados
        st.write(f"**{len(resultados)} estabelecimento(s) encontrado(s)**")

        if resultados:
            df = pd.DataFrame([asdict(e) for e in resultados])
            st.dataframe(
                df[
                    [
                        "nome",
                        "bairro",
                        "tipo_negocio",
                        "tem_site",
                        "potencial_cliente",
                        "prioridade_contato",
                    ]
                ],
                use_container_width=True,
            )

            # Detalhes expandíveis
            for est in resultados:
                with st.expander(f"📋 {est.nome}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Informações Básicas**")
                        st.write(f"📍 {est.endereco}")
                        st.write(f"🏘️ {est.bairro}")
                        st.write(f"🏪 {est.tipo_negocio}")
                        st.write(f"⭐ Prioridade: {est.prioridade_contato}/5")

                    with col2:
                        st.write("**Presença Digital**")
                        st.write(f"Website: {'✅' if est.tem_site else '❌'}")
                        st.write(f"Instagram: {'✅' if est.tem_instagram else '❌'}")
                        st.write(f"Facebook: {'✅' if est.tem_facebook else '❌'}")
                        st.write(
                            f"Google Business: {'✅' if est.tem_google_business else '❌'}"
                        )

                    if est.oportunidades:
                        st.write("**💡 Oportunidades**")
                        for op in est.oportunidades:
                            st.write(f"• {op}")

                    if est.observacoes:
                        st.write("**📝 Observações**")
                        st.write(est.observacoes)

# PRÓXIMOS CONTATOS
elif menu == "Próximos Contatos":
    st.title("🎯 Próximos Contatos Prioritários")

    nao_contatados = [
        e for e in sistema.estabelecimentos if e.status_contato == "Não contatado"
    ]

    if not nao_contatados:
        st.success("🎉 Todos os estabelecimentos foram contatados!")
    else:
        prioritarios = sorted(
            nao_contatados, key=lambda x: x.prioridade_contato, reverse=True
        )

        st.write(f"**{len(prioritarios)} estabelecimento(s) aguardando contato**")

        for i, est in enumerate(prioritarios[:20], 1):
            with st.container():
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.subheader(f"{i}. {est.nome}")
                    st.write(f"📍 {est.endereco}, {est.bairro}")
                    st.write(f"🏪 {est.tipo_negocio}")

                    if est.oportunidades:
                        st.write("**💡 Principais oportunidades:**")
                        for op in est.oportunidades[:3]:
                            st.write(f"• {op}")

                with col2:
                    st.metric("Prioridade", f"{est.prioridade_contato}/5")
                    st.write(f"**Potencial:** {est.potencial_cliente}")

                    if st.button(f"Marcar como Contatado", key=f"contato_{i}"):
                        est.status_contato = "Contatado"
                        sistema.salvar_dados()
                        st.rerun()

                st.divider()

# RELATÓRIOS
elif menu == "Relatórios":
    st.title("📊 Relatórios e Análises")

    if not sistema.estabelecimentos:
        st.warning("Nenhum estabelecimento mapeado ainda.")
    else:
        # Seletor de bairro
        bairros = ["Todos"] + sorted(
            list(set(e.bairro for e in sistema.estabelecimentos))
        )
        bairro_selecionado = st.selectbox("Selecionar Bairro", bairros)

        estabelecimentos = sistema.estabelecimentos
        if bairro_selecionado != "Todos":
            estabelecimentos = [
                e for e in estabelecimentos if e.bairro == bairro_selecionado
            ]

        # Estatísticas
        total = len(estabelecimentos)
        sem_site = len([e for e in estabelecimentos if not e.tem_site])
        sem_instagram = len([e for e in estabelecimentos if not e.tem_instagram])
        alta_prioridade = len(
            [e for e in estabelecimentos if e.prioridade_contato >= 4]
        )

        st.subheader("📈 Estatísticas Gerais")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total", total)
        col2.metric(
            "Sem Website",
            f"{sem_site} ({sem_site/total*100:.0f}%)" if total > 0 else "0",
        )
        col3.metric(
            "Sem Instagram",
            f"{sem_instagram} ({sem_instagram/total*100:.0f}%)" if total > 0 else "0",
        )
        col4.metric(
            "Alta Prioridade",
            (
                f"{alta_prioridade} ({alta_prioridade/total*100:.0f}%)"
                if total > 0
                else "0"
            ),
        )

        # Tabela completa
        st.subheader("📋 Dados Completos")
        df = pd.DataFrame([asdict(e) for e in estabelecimentos])
        st.dataframe(df, use_container_width=True)

        # Botão de exportação
        if st.button("📥 Exportar para CSV"):
            sistema.exportar_para_csv()
            st.success("✅ Dados exportados para 'dados/estabelecimentos.csv'")

# Footer
st.sidebar.markdown("---")
st.sidebar.info(f"📊 **{len(sistema.estabelecimentos)}** estabelecimentos mapeados")
st.sidebar.markdown("**Ávila - Lisboa Expansion Project**")
