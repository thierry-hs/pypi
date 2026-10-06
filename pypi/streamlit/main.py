import random
import pandas as pd
import streamlit as st

# Configuração principal da página
st.set_page_config(
    page_title="Clash Royale Hub ⚔️",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilização CSS personalizada
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
    }
    .card-box {
        background: linear-gradient(135deg, #1f2937, #111827);
        border: 2px solid #f59e0b;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    .elixir-drop {
        background-color: #a855f7;
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9em;
    }
    .stat-card {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Base de dados de cartas
CARDS_DATA = [
    {
        "Nome": "Corredor",
        "Raridade": "Rara",
        "Tipo": "Tropa",
        "Elixir": 4,
        "Funcao": "Condicao de Vitoria",
        "Icone": "🔨",
        "Descricao": "Tropa rápida voltada para construções e torres inimigas.",
    },
    {
        "Nome": "P.E.K.K.A",
        "Raridade": "Épica",
        "Tipo": "Tropa",
        "Elixir": 7,
        "Funcao": "Tanque / Defesa",
        "Icone": "🤖",
        "Descricao": "Poderosa defensora terrestre com alto dano por golpe.",
    },
    {
        "Nome": "O Tronco",
        "Raridade": "Lendária",
        "Tipo": "Feitiço",
        "Elixir": 2,
        "Funcao": "Controle de Grupo",
        "Icone": "🪵",
        "Descricao": "Elimina tropas terrestres leves e empurra os inimigos.",
    },
    {
        "Nome": "Megacavaleiro",
        "Raridade": "Lendária",
        "Tipo": "Tropa",
        "Elixir": 7,
        "Funcao": "Tanque / Dano em Área",
        "Icone": "🛡️",
        "Descricao": "Aterra com impacto gerando dano em área e salta sobre tropas.",
    },
    {
        "Nome": "Mago Elétrico",
        "Raridade": "Lendária",
        "Tipo": "Tropa",
        "Elixir": 4,
        "Funcao": "Suporte / Atordoamento",
        "Icone": "⚡",
        "Descricao": "Reseta carregamentos de P.E.K.K.A, Torre Inferno e Dragão Infernal.",
    },
    {
        "Nome": "Bola de Fogo",
        "Raridade": "Rara",
        "Tipo": "Feitiço",
        "Elixir": 4,
        "Funcao": "Dano Direto",
        "Icone": "🔥",
        "Descricao": "Feitiço versátil para dano em área médio/alto.",
    },
    {
        "Nome": "Torre Inferno",
        "Raridade": "Rara",
        "Tipo": "Construção",
        "Elixir": 5,
        "Funcao": "Defesa Antitanque",
        "Icone": "🏰",
        "Descricao": "Aumenta o dano progressivamente destruindo tropas de alta vida.",
    },
    {
        "Nome": "Goleirinho / Pequeno Príncipe",
        "Raridade": "Campeão",
        "Tipo": "Tropa",
        "Elixir": 3,
        "Funcao": "Suporte / Habilidade",
        "Icone": "👑",
        "Descricao": "Ataca à distância com velocidade crescente e invoca o Guarda real.",
    },
    {
        "Nome": "Bebê Dragão",
        "Raridade": "Épica",
        "Tipo": "Tropa",
        "Elixir": 4,
        "Funcao": "Dano em Área Aéreo",
        "Icone": "🐉",
        "Descricao": "Unidade aérea voadora resistente com dano em área.",
    },
    {
        "Nome": "Goblins de Lança",
        "Raridade": "Comum",
        "Tipo": "Tropa",
        "Elixir": 2,
        "Funcao": "Ciclo / Suporte",
        "Icone": "🗡️",
        "Descricao": "Três tropas rápidas e baratas para ataque aéreo e terrestre.",
    },
    {
        "Nome": "Espírito Elétrico",
        "Raridade": "Comum",
        "Tipo": "Tropa",
        "Elixir": 1,
        "Funcao": "Ciclo / Atordoamento",
        "Icone": "🔋",
        "Descricao": "Gera corrente elétrica atordoando até 9 alvos.",
    },
    {
        "Nome": "Lança-Dardos",
        "Raridade": "Rara",
        "Tipo": "Tropa",
        "Elixir": 3,
        "Funcao": "Dano Rápido à Distância",
        "Icone": "🎯",
        "Descricao": "Lança dardos em altíssima velocidade com longo alcance.",
    },
]

df_cards = pd.DataFrame(CARDS_DATA)

# Cabeçalho da aplicação
st.title("⚔️ Clash Royale Strategy Hub & Deck Builder")
st.caption(
    "Analise cartas, monte decks equilibrados e calcule estratégias de Elixir!"
)

# Barra lateral com estatísticas gerais
st.sidebar.header("👑 Estatísticas da Base")
st.sidebar.metric("Total de Cartas no App", len(df_cards))
st.sidebar.metric(
    "Custo Médio de Elixir", f"{df_cards['Elixir'].mean():.2f} 🧪"
)

rarity_filter = st.sidebar.multiselect(
    "Filtrar por Raridade:",
    options=df_cards["Raridade"].unique(),
    default=df_cards["Raridade"].unique(),
)

df_filtered = df_cards[df_cards["Raridade"].isin(rarity_filter)]

# Abas principais
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🎴 Explorador de Cartas",
        "🛡️ Montador de Deck",
        "🧪 Calculadora de Elixir",
        "🎯 Quiz Royale",
    ]
)

# --- ABA 1: EXPLORADOR DE CARTAS ---
with tab1:
    st.subheader("Biblioteca de Cartas")

    col_search, col_type, col_elixir = st.columns([2, 1, 1])

    with col_search:
        search_query = st.text_input(
            "Buscar por nome da carta:", placeholder="Ex: Corredor..."
        )
    with col_type:
        type_filter = st.selectbox(
            "Tipo de Carta:", ["Todos"] + list(df_cards["Tipo"].unique())
        )
    with col_elixir:
        max_elixir = st.slider("Custo Máximo de Elixir:", 1, 7, 7)

    # Filtragem
    df_display = df_filtered[df_filtered["Elixir"] <= max_elixir]
    if search_query:
        df_display = df_display[
            df_display["Nome"].str.contains(search_query, case=False)
        ]
    if type_filter != "Todos":
        df_display = df_display[df_display["Tipo"] == type_filter]

    # Grid de exibições
    cols = st.columns(3)
    for index, card in df_display.reset_index(drop=True).iterrows():
        with cols[index % 3]:
            st.markdown(
                f"""
                <div class="card-box">
                    <h3>{card['Icone']} {card['Nome']}</h3>
                    <p><span class="elixir-drop">🧪 {card['Elixir']} Elixir</span> | <b>{card['Raridade']}</b></p>
                    <p><b>Tipo:</b> {card['Tipo']} ({card['Funcao']})</p>
                    <p style="font-size: 0.85em; color: #cbd5e1;">{card['Descricao']}</p>
                </div>
            """,
                unsafe_allow_html=True,
            )

# --- ABA 2: MONTADOR DE DECK ---
with tab2:
    st.subheader("Monte seu Deck de 8 Cartas")

    selected_cards = st.multiselect(
        "Escolha exatamente 8 cartas para a análise do seu deck:",
        options=df_cards["Nome"].tolist(),
        max_selections=8,
    )

    if len(selected_cards) == 8:
        deck_df = df_cards[df_cards["Nome"].isin(selected_cards)]
        avg_elixir = deck_df["Elixir"].mean()

        st.success(f" Deck Completo! Custo Médio de Elixir: **{avg_elixir:.2f}**")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Custo Médio de Elixir", f"{avg_elixir:.2f} 🧪")
            if avg_elixir < 3.3:
                st.info("⚡ Deck Ciclo Rápido: Permite rodar cartas velozmente.")
            elif avg_elixir <= 4.2:
                st.info("⚖️ Deck Equilibrado: Bom controle de jogo e pressão.")
            else:
                st.warning(
                    "🐘 Deck Beatdown/Pesado: Requer cuidado com gestão de elixir."
                )

        with c2:
            win_conditions = deck_df[
                deck_df["Funcao"].str.contains("Condicao", case=False)
            ]
            st.metric("Condições de Vitória", len(win_conditions))
            if len(win_conditions) == 0:
                st.error("⚠️ Atenção: Seu deck não possui uma Carta de Ataque Principal clara.")

        with c3:
            spells = deck_df[deck_df["Tipo"] == "Feitiço"]
            st.metric("Feitiços no Deck", len(spells))
            if len(spells) == 0:
                st.warning("💡 Dica: Adicionar pelo menos 1 feitiço ajuda na finalização.")

        st.subheader("Sua Seleção:")
        deck_cols = st.columns(4)
        for idx, row in deck_df.reset_index(drop=True).iterrows():
            with deck_cols[idx % 4]:
                st.markdown(
                    f"**{row['Icone']} {row['Nome']}** ({row['Elixir']} 🧪)"
                )

    else:
        st.info(f"Selecione mais {8 - len(selected_cards)} carta(s) para completar a análise.")

# --- ABA 3: CALCULADORA DE ELIXIR ---
with tab3:
    st.subheader("Simulador de Tempo de Gerador de Elixir")

    st.write(
        "Entenda o ritmo da partida para planejar pushes nos momentos certos!"
    )

    fase = st.radio(
        "Fase da Partida:",
        ["Elixir Normal (1x)", "Elixir Duplo (2x)", "Elixir Triplo (3x)"],
        horizontal=True,
    )

    taxa_map = {
        "Elixir Normal (1x)": 2.8,  # 1 gota a cada 2.8s
        "Elixir Duplo (2x)": 1.4,
        "Elixir Triplo (3x)": 0.9,
    }

    tempo_gota = taxa_map[fase]
    elixir_desejado = st.slider("Quantidade de Elixir necessária:", 1, 10, 10)

    tempo_total = elixir_desejado * tempo_gota

    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.markdown(
            f"""
            <div class="stat-card">
                <h3>⏱️ Tempo de Espera</h3>
                <h2>{tempo_total:.1f} segundos</h2>
                <p>Para gerar {elixir_desejado} gotas no modo <b>{fase}</b>.</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col_res2:
        st.markdown(
            """
            ### 💡 Dicas Estratégicas:
            - **1x Elixir:** Foque em defender bem e descobrir as cartas do oponente.
            - **2x Elixir:** Excelente momento para montar um ataque completo (Push).
            - **3x Elixir:** Mantenha o ritmo alto e não deixe o adversário acumular tropas.
        """
        )

# --- ABA 4: QUIZ ROYALE ---
with tab4:
    st.subheader("Testes seus Conhecimentos de Clash Royale!")

    score = 0

    q1 = st.radio(
        "1. Qual carta atordoa tropas e reseta a torre inferno ao ser posicionada?",
        [
            "Mago de Fogo",
            "Mago Elétrico",
            "Bebê Dragão",
            "Cavaleiro",
        ],
    )
    if q1 == "Mago Elétrico":
        score += 1

    q2 = st.radio(
        "2. Quanto custa a carta O Tronco?",
        ["1 Elixir", "2 Elixir", "3 Elixir", "4 Elixir"],
    )
    if q2 == "2 Elixir":
        score += 1

    q3 = st.radio(
        "3. Qual destas tropas tem como foco exclusivo atacar edifícios?",
        ["P.E.K.K.A", "Megacavaleiro", "Corredor", "Lança-Dardos"],
    )
    if q3 == "Corredor":
        score += 1

    if st.button("Verificar Resultado do Quiz"):
        if score == 3:
            st.balloons()
            st.success(
                f"Parabéns! Você acertou {score}/3 e ganhou o Baú Lendário! 🏆"
            )
        else:
            st.warning(f"Você acertou {score}/3 perguntas. Tente novamente!")