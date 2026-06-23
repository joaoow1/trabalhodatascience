# ⚽ Análise de Jogadores de Futebol — Projeto de Data Science

Projeto final da disciplina de **Data Science**. A partir dos atributos de
~17 mil jogadores de futebol (base do FIFA 22), o trabalho investiga o que
determina o **valor de mercado** de um jogador, constrói modelos para **prevê-lo**
e usa aprendizado não-supervisionado para descobrir **perfis** de jogadores —
seguindo um fluxo completo de ciência de dados, da coleta à comunicação dos
resultados em um dashboard interativo.

> **Repositório:** https://github.com/joaoow1/trabalhodatascience
> **Dashboard online:** https://trabalhodatascience-m4yyawhcs6hnbunakukzdb.streamlit.app
> **Autor(es):** João Otávio Quevedo, Eduardo Hoppen, Leonardo Cologneze e Mateus Gomes

---

## 📌 Tema e objetivo

O projeto se coloca no lugar da área de análise de um clube/empresário e busca
responder três perguntas:

1. **Quais fatores determinam o valor de mercado de um jogador?**
2. **É possível prever esse valor a partir dos atributos? Qual modelo erra menos:
   Regressão Linear ou KNN?**
3. **Os atributos técnicos agrupam os jogadores em perfis que correspondem às
   posições reais em campo?** (K-Means)

---

## 🗂️ Estrutura do repositório

```
trabalhodatascience/
├── README.md
├── requirements.txt
├── data/
│   ├── players_clean.csv          # dataset limpo  (saída do notebook 01)
│   └── players_clusters.csv       # dataset + clusters (saída do notebook 03)
├── notebooks/
│   ├── 01_limpeza.ipynb           # coleta, limpeza e preparação dos dados
│   ├── 02_eda.ipynb               # análise exploratória e teste das hipóteses
│   └── 03_modelagem.ipynb         # K-Means + Regressão Linear vs. KNN
├── models/
│   ├── modelo_regressao.joblib    # modelo de valor treinado (Regressão Linear)
│   └── metadados.json             # features e medianas usadas pelo dashboard
└── dashboard/
    └── app.py                     # dashboard interativo (Streamlit)
```

> O CSV bruto (`players_22.csv`, ~13 MB) **não é versionado**: o notebook
> `01_limpeza.ipynb` o baixa automaticamente na primeira execução.

---

## 📊 Dataset

- **Origem:** *FIFA 22 complete player dataset*, raspado do site
  [sofifa.com](https://sofifa.com) (que, conforme seu `robots.txt`, não restringe
  a coleta de dados de jogadores). Cópia pública utilizada:
  [GitHub — abineshta/FIFA-22-complete-player-dataset-EDA](https://github.com/abineshta/FIFA-22-complete-player-dataset-EDA).
- **Volume:** 19.239 jogadores e 110 colunas no dado bruto →
  **17.041 jogadores de linha e 61 variáveis** após a limpeza.
- **Variável-alvo:** `value_eur` (valor de mercado em euros); modelada em escala
  logarítmica (`value_log`).
- **Principais grupos de variáveis:**
  - *Identificação:* nome, clube, liga, nacionalidade.
  - *Perfil:* idade, altura, peso, `overall`, `potential`, posição, reputação.
  - *Atributos técnicos (0–100):* 6 agregados (`pace`, `shooting`, `passing`,
    `dribbling`, `defending`, `physic`) e 29 detalhados (finalização, drible,
    desarme, etc.).

### Transformações realizadas (notebook 01)

- **Seleção** de 55 colunas relevantes (de 110), descartando URLs, dados esparsos
  e os ratings por posição em formato textual.
- **Remoção da cláusula de rescisão** (`release_clause_eur`) para evitar
  *data leakage*, por ser praticamente uma função do valor de mercado.
- **Separação dos goleiros** (~2,1 mil), que não possuem atributos de jogador de
  linha — sua ausência nos dados era estrutural, não aleatória.
- **Imputação** de ausentes residuais pela mediana.
- **Engenharia de features:** `field_sector` (setor de campo), `potential_gap`
  (potencial − overall), `bmi`, `value_log` e `wage_log`.
- **Transformação logarítmica** do valor, justificada pela forte assimetria da
  distribuição.

---

## 🔬 Metodologia

| Etapa | Notebook | Conteúdo |
|---|---|---|
| Coleta, limpeza e preparação | `01_limpeza.ipynb` | importação, seleção de colunas, tratamento de ausentes, engenharia de features |
| Análise exploratória | `02_eda.ipynb` | estatísticas descritivas, visualizações e teste das 4 hipóteses |
| Modelagem e avaliação | `03_modelagem.ipynb` | K-Means (perfis) + Regressão Linear vs. KNN (valor) |
| Comunicação | `dashboard/app.py` | dashboard interativo com os principais resultados |

---

## 🤖 Modelos utilizados

- **K-Means** (não-supervisionado): agrupa os jogadores pelos 29 atributos
  técnicos padronizados. O número de clusters (**k = 3**) foi definido pelo método
  do cotovelo e pelo coeficiente de silhueta, e escolhido também para permitir a
  comparação direta com os três setores de campo.
- **Regressão Linear** (supervisionado): prevê `value_log` a partir do perfil e dos
  atributos. **Não utiliza o salário como preditor** (evita *near-leakage*).
- **K-Nearest Neighbors (KNN)** (supervisionado): mesma tarefa, com o número de
  vizinhos *k* escolhido por validação cruzada (5 folds).

---

## 📈 Resultados

### Hipóteses (notebook 02)

| Hipótese | Resultado |
|---|---|
| **H1** — relação overall × valor é exponencial | ✅ Confirmada (correlação sobe de 0,56 para **0,91** ao usar o log) |
| **H2** — a idade tem efeito não-linear no valor | ✅ Confirmada (pico por volta dos **23 anos**, com platô até ~27) |
| **H3** — atacantes valem mais (mesmo overall) | 🔴 Refutada — o "prêmio" de valor é do **meio-campo**, não do ataque |
| **H4** — os atributos separam os jogadores por posição | ✅ Confirmada (heatmap, PCA e clusterização) |

### Modelagem (notebook 03)

**Previsão de valor — comparação dos modelos (conjunto de teste):**

| Modelo | R² | RMSE (log) | MAE (€) |
|---|---|---|---|
| **Regressão Linear** ✅ | **0,973** | 0,197 | ~605 mil |
| KNN (k = 9) | 0,918 | 0,346 | ~1,01 mi |

A **Regressão Linear** apresentou o melhor desempenho e foi salva como modelo
principal, usada no simulador do dashboard. O R² elevado é esperado: no FIFA, o
valor de mercado é, em boa parte, derivado das próprias notas do jogador.

**Perfis (K-Means):** os clusters formados apenas a partir dos atributos técnicos
recuperaram cerca de **65% dos setores de campo reais** (contra ~33% de um palpite
aleatório), com perfis nítidos (defensivo, meio-campo e ofensivo) — dando suporte
quantitativo à hipótese H4.

---

## 🚀 Como executar

### Pré-requisitos
- Python 3.10+
- Instalar as dependências:
  ```bash
  pip install -r requirements.txt
  ```

### Notebooks
Execute na ordem (`01` → `02` → `03`). O primeiro baixa o dado bruto
automaticamente e gera `data/players_clean.csv`; o terceiro gera
`data/players_clusters.csv` e os artefatos em `models/`.

### Dashboard interativo
Na raiz do projeto:
```bash
streamlit run dashboard/app.py
```
O dashboard abre em `http://localhost:8501` e possui três abas: **Explorador**
(filtros e gráficos), **Perfis** (clusters do K-Means) e **Simulador de Valor**
(ajuste os atributos e veja o valor previsto pelo modelo).

> **Dashboard online:** https://trabalhodatascience-m4yyawhcs6hnbunakukzdb.streamlit.app

---

## 👤 Autor(es)
- João Otávio Quevedo
- Eduardo Hoppen
- Leonardo Cologneze
- Mateus Gomes
