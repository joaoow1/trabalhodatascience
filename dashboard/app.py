"""
Dashboard interativo — Projeto de Data Science (Jogadores de Futebol)
====================================================================
Três abas:
  1. Explorador  — filtros (liga, posição, idade, overall) + gráficos
  2. Perfis      — visualização dos clusters do K-Means
  3. Simulador   — sliders de atributos -> o modelo prevê o valor de mercado

Como executar localmente:
  pip install -r requirements.txt
  streamlit run dashboard/app.py
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import joblib

# ---------------------------------------------------------------------------
# Configuração de caminhos (relativos à raiz do repositório)
# ---------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "data"
MODELS_DIR = BASE / "models"

ATTRS_AGG = ["pace", "shooting", "passing", "dribbling", "defending", "physic"]
SETOR_CORES = {"Defensor": "#2471a3", "Meio-campo": "#16a085", "Atacante": "#c0392b"}

st.set_page_config(page_title="DS Futebol — Dashboard", page_icon="⚽", layout="wide")


# ---------------------------------------------------------------------------
# Carga de dados e modelo (com cache para não recarregar a cada interação)
# ---------------------------------------------------------------------------
@st.cache_data
def carregar_dados():
    df = pd.read_csv(DATA_DIR / "players_clusters.csv")
    return df


@st.cache_resource
def carregar_modelo():
    modelo = joblib.load(MODELS_DIR / "modelo_regressao.joblib")
    with open(MODELS_DIR / "metadados.json", encoding="utf-8") as f:
        meta = json.load(f)
    return modelo, meta


df = carregar_dados()
modelo, meta = carregar_modelo()

# Mapa cluster -> nome (setor majoritário) para legendas amigáveis
_maj = df.groupby("cluster")["field_sector"].agg(lambda s: s.mode()[0])
NOME_CLUSTER = {c: f"Cluster {c} · {_maj[c]}" for c in sorted(df["cluster"].unique())}
df["cluster_nome"] = df["cluster"].map(NOME_CLUSTER)


# ---------------------------------------------------------------------------
# Cabeçalho e barra lateral
# ---------------------------------------------------------------------------
st.title("⚽ Análise de Jogadores de Futebol — FIFA 22")
st.caption("Valor de mercado, perfis de jogadores e simulação · dados do Sofifa (FIFA 22)")

with st.sidebar:
    st.header("Sobre o projeto")
    st.markdown(
        """
        Projeto de **Data Science** que investiga, a partir dos atributos de
        ~17 mil jogadores de linha:

        1. O que determina o **valor de mercado**.
        2. Se é possível **prevê-lo** (Regressão Linear vs. KNN).
        3. Se os atributos formam **perfis** que correspondem às posições (K-Means).
        """
    )
    st.divider()
    st.metric("Jogadores", f"{len(df):,}".replace(",", "."))
    st.metric(f"Modelo de valor: {meta['modelo_principal']}",
              f"R² = {meta['metricas']['r2_linear']:.3f}")


# ---------------------------------------------------------------------------
# Abas
# ---------------------------------------------------------------------------
aba_exp, aba_perfis, aba_sim = st.tabs(
    ["🔎 Explorador", "🧭 Perfis (clusters)", "🎚️ Simulador de Valor"])


# ===========================================================================
# ABA 1 — EXPLORADOR
# ===========================================================================
with aba_exp:
    st.subheader("Explorador de jogadores")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        ligas = sorted(df["league_name"].dropna().unique())
        ligas_sel = st.multiselect("Liga", ligas, default=[],
                                   help="Vazio = todas as ligas")
    with c2:
        setores = ["Defensor", "Meio-campo", "Atacante"]
        setores_sel = st.multiselect("Posição (setor)", setores, default=setores)
    with c3:
        idade_min, idade_max = int(df["age"].min()), int(df["age"].max())
        faixa_idade = st.slider("Idade", idade_min, idade_max,
                                (idade_min, idade_max))
    with c4:
        ov_min, ov_max = int(df["overall"].min()), int(df["overall"].max())
        faixa_overall = st.slider("Overall", ov_min, ov_max, (ov_min, ov_max))

    # Aplica os filtros
    f = df.copy()
    if ligas_sel:
        f = f[f["league_name"].isin(ligas_sel)]
    if setores_sel:
        f = f[f["field_sector"].isin(setores_sel)]
    f = f[(f["age"].between(*faixa_idade)) & (f["overall"].between(*faixa_overall))]

    st.markdown(f"**{len(f):,}** jogadores correspondem aos filtros."
                .replace(",", "."))

    if len(f) == 0:
        st.warning("Nenhum jogador encontrado. Ajuste os filtros.")
    else:
        col_a, col_b = st.columns([3, 2])
        with col_a:
            # Dispersão overall x valor (amostra para manter fluido)
            amostra = f.sample(min(3000, len(f)), random_state=42)
            fig = px.scatter(
                amostra, x="overall", y="value_eur", color="field_sector",
                color_discrete_map=SETOR_CORES, hover_name="short_name",
                hover_data={"club_name": True, "age": True, "value_eur": ":,.0f"},
                labels={"overall": "Overall", "value_eur": "Valor (€)",
                        "field_sector": "Setor"},
                title="Overall × Valor de mercado")
            fig.update_yaxes(type="log")
            st.plotly_chart(fig, use_container_width=True)
        with col_b:
            # Top 10 mais valiosos do recorte
            top = (f.nlargest(10, "value_eur")[["short_name", "club_name", "value_eur"]]
                   .reset_index(drop=True))
            top["value_eur"] = (top["value_eur"] / 1e6).round(1)
            top.columns = ["Jogador", "Clube", "Valor (M€)"]
            st.markdown("**Top 10 mais valiosos**")
            st.dataframe(top, use_container_width=True, hide_index=True)

        # Tabela detalhada
        st.markdown("**Lista de jogadores**")
        cols_tab = ["short_name", "club_name", "league_name", "field_sector",
                    "age", "overall", "potential", "value_eur"]
        tabela = f[cols_tab].sort_values("value_eur", ascending=False).copy()
        tabela["value_eur"] = (tabela["value_eur"] / 1e6).round(2)
        tabela.columns = ["Jogador", "Clube", "Liga", "Setor", "Idade",
                          "Overall", "Potential", "Valor (M€)"]
        st.dataframe(tabela, use_container_width=True, hide_index=True, height=320)


# ===========================================================================
# ABA 2 — PERFIS (CLUSTERS)
# ===========================================================================
with aba_perfis:
    st.subheader("Perfis de jogadores (K-Means)")
    st.markdown(
        "Os grupos abaixo foram formados **apenas a partir dos atributos técnicos**, "
        "sem informar a posição. Compare os clusters com os setores reais para ver "
        "o quanto os dados 'sabem' onde o jogador atua.")

    col1, col2 = st.columns([3, 2])
    with col1:
        colorir = st.radio("Colorir a projeção por:",
                           ["Cluster", "Setor real"], horizontal=True)
        amostra = df.sample(min(4000, len(df)), random_state=42)
        if colorir == "Cluster":
            fig = px.scatter(amostra, x="PC1", y="PC2", color="cluster_nome",
                             hover_name="short_name",
                             hover_data={"field_sector": True, "PC1": False,
                                         "PC2": False},
                             title="Projeção PCA dos atributos")
        else:
            fig = px.scatter(amostra, x="PC1", y="PC2", color="field_sector",
                             color_discrete_map=SETOR_CORES,
                             hover_name="short_name",
                             hover_data={"cluster_nome": True, "PC1": False,
                                         "PC2": False},
                             title="Projeção PCA dos atributos")
        fig.update_layout(legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Radar com o perfil médio de cada cluster (6 atributos agregados)
        perfil = df.groupby("cluster")[ATTRS_AGG].mean()
        radar = go.Figure()
        for c in perfil.index:
            valores = perfil.loc[c].tolist()
            radar.add_trace(go.Scatterpolar(
                r=valores + [valores[0]],
                theta=ATTRS_AGG + [ATTRS_AGG[0]],
                fill="toself", name=NOME_CLUSTER[c]))
        radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 90])),
            showlegend=True, title="Perfil médio de cada cluster",
            legend=dict(orientation="h", yanchor="bottom", y=-0.3))
        st.plotly_chart(radar, use_container_width=True)

    # Resumo numérico dos clusters
    resumo = df.groupby("cluster_nome").agg(
        n_jogadores=("sofifa_id", "size"),
        overall_medio=("overall", "mean"),
        valor_mediano=("value_eur", lambda x: round(x.median() / 1e6, 2)),
    ).round(1).reset_index()
    resumo.columns = ["Cluster", "Jogadores", "Overall médio", "Valor mediano (M€)"]
    st.dataframe(resumo, use_container_width=True, hide_index=True)


# ===========================================================================
# ABA 3 — SIMULADOR DE VALOR
# ===========================================================================
with aba_sim:
    st.subheader("Simulador de valor de mercado")
    st.markdown(
        f"Ajuste os atributos de um jogador hipotético e veja o valor estimado pelo "
        f"modelo (**{meta['modelo_principal']}**). Os demais atributos ficam fixados "
        f"na mediana da base.")

    medianas = meta["medianas"]
    esq, dir_ = st.columns(2)
    with esq:
        v_age = st.slider("Idade", 16, 45, int(medianas["age"]))
        v_overall = st.slider("Overall", 40, 95, int(medianas["overall"]))
        v_potential = st.slider("Potential", 40, 99, int(medianas["potential"]))
        v_reput = st.slider("Reputação internacional", 1, 5,
                            int(medianas["international_reputation"]))
        v_setor = st.selectbox("Setor de campo", meta["setores"], index=1)
    with dir_:
        v_pace = st.slider("Pace", 20, 99, int(medianas["pace"]))
        v_shooting = st.slider("Shooting", 20, 99, int(medianas["shooting"]))
        v_passing = st.slider("Passing", 20, 99, int(medianas["passing"]))
        v_dribbling = st.slider("Dribbling", 20, 99, int(medianas["dribbling"]))
        v_defending = st.slider("Defending", 20, 99, int(medianas["defending"]))
        v_physic = st.slider("Physic", 20, 99, int(medianas["physic"]))

    # Monta a linha de entrada: começa nas medianas e sobrescreve o que foi ajustado
    linha = dict(medianas)
    linha.update({
        "age": v_age, "overall": v_overall, "potential": v_potential,
        "international_reputation": v_reput, "pace": v_pace, "shooting": v_shooting,
        "passing": v_passing, "dribbling": v_dribbling, "defending": v_defending,
        "physic": v_physic,
    })
    # Recalcula a feature derivada para manter coerência
    linha["potential_gap"] = linha["potential"] - linha["overall"]
    linha["field_sector"] = v_setor

    X_in = pd.DataFrame([linha])[meta["features_num"] + meta["features_cat"]]
    valor_log = modelo.predict(X_in)[0]
    valor = float(np.expm1(valor_log))
    percentil = (df["value_eur"] < valor).mean() * 100

    st.divider()
    m1, m2 = st.columns(2)
    m1.metric("💰 Valor de mercado estimado", f"€ {valor:,.0f}".replace(",", "."))
    m2.metric("Posição na base", f"mais valioso que {percentil:.0f}% dos jogadores")
    st.caption("Estimativa baseada no modelo treinado no notebook 03. "
               "Os atributos não exibidos (técnicos detalhados, físico) usam a mediana da base.")
