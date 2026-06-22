# 002 — Finalização do GitHub

## Objetivo

Garantir que o repositório remoto contenha todos os arquivos necessários, documentação completa e histórico final verificável.

## Requisitos funcionais

- Versionar `dashboard/app.py`, `requirements.txt`, `README.md`, documentação e artefatos necessários.
- Preencher no README autoria, URL correta do repositório e link público do dashboard quando disponível.
- Manter instruções de instalação e execução compatíveis com o projeto atual.

## Requisitos técnicos

- A árvore rastreada não deve conter credenciais, ambientes virtuais, checkpoints ou dataset bruto grande.
- `requirements.txt` deve permitir instalar as dependências em Python 3.10+.
- Commits devem ter assunto curto e descritivo; o branch remoto final deve estar sincronizado.

## Testes e validações

- Executar `git status`, `git diff --check` e revisar `git diff --stat`.
- Clonar ou testar em ambiente limpo: instalar requisitos e iniciar `streamlit run dashboard/app.py`.
- Abrir todos os links do README e confirmar arquivos na interface do GitHub.

## Critérios mínimos de aceite

- Arquivos obrigatórios aparecem no GitHub e o working tree final está limpo.
- README não contém marcadores como `*(preencher)*` ou URLs incorretas.
- Uma instalação limpa inicia o dashboard sem erro.

## Tarefas de implementação

1. Auditar arquivos rastreados, pendentes e ignorados.
2. Confirmar nome do autor e URL canônica do repositório.
3. Atualizar os campos e comandos do README.
4. Validar instalação e execução em ambiente limpo.
5. Revisar alterações e remover dados sensíveis ou arquivos indevidos.
6. Criar commits descritivos e enviar o branch ao GitHub.
7. Conferir o conteúdo publicado e registrar o link do dashboard após a spec 003.
