# 001 — Relatório técnico em PDF

## Objetivo

Consolidar a análise atualmente distribuída nos notebooks e no README em um relatório acadêmico único, reproduzível e pronto para avaliação.

## Requisitos funcionais

- Conter Introdução, Dataset, EDA, Modelagem, Resultados e Discussão, Conclusão e Referências.
- Explicar objetivo, hipóteses, preparação dos dados, escolhas dos modelos e limitações.
- Incluir gráficos e tabelas legíveis, numerados e mencionados no texto.
- Apresentar as métricas finais da Regressão Linear, KNN e K-Means sem divergências em relação aos notebooks.

## Requisitos técnicos

- Fonte em Markdown ou Jupyter Notebook versionada em `docs/`.
- PDF gerado em `docs/relatorio-tecnico.pdf`, com fontes incorporadas e páginas em tamanho A4.
- Imagens com resolução suficiente para leitura a 100% de zoom; links e referências devem funcionar.
- Não depender de caminhos absolutos nem de execução manual de células fora de ordem.

## Testes e validações

- Exportar a fonte do zero sem erros ou conteúdo ausente.
- Conferir visualmente todas as páginas, quebras, acentos, legendas e referências.
- Comparar números, amostras e métricas com `README.md` e notebooks `01` a `03`.
- Confirmar que o PDF abre em outro leitor e permite busca de texto.

## Critérios mínimos de aceite

- Todas as seções obrigatórias estão presentes e coerentes.
- Não há gráficos cortados, páginas vazias indevidas ou valores contraditórios.
- O PDF final está versionado e possui autoria, título e data.

## Tarefas de implementação

1. Definir a fonte do relatório e criar seu esqueleto em `docs/`.
2. Consolidar Introdução e descrição do Dataset a partir do README e notebook 01.
3. Sintetizar EDA e hipóteses com os gráficos essenciais do notebook 02.
4. Documentar modelagem, avaliação e comparação usando o notebook 03.
5. Redigir Resultados e Discussão, Conclusão, limitações e referências.
6. Padronizar figuras, tabelas, títulos, autoria e citações.
7. Exportar o PDF e executar todas as validações desta spec.
8. Fazer revisão final de conteúdo e linguagem.
