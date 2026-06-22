# 003 — Publicação no Streamlit Community Cloud

## Objetivo

Disponibilizar uma demonstração pública e estável do dashboard, vinculada ao repositório GitHub.

## Requisitos funcionais

- Exibir as três abas, filtros, visualizações e simulador de valor.
- Disponibilizar uma URL pública permanente e registrá-la no README.
- Mostrar mensagens compreensíveis caso dados ou modelo não possam ser carregados.

## Requisitos técnicos

- Repositório acessível pelo Streamlit Cloud, com entry point `dashboard/app.py`.
- Dependências declaradas em `requirements.txt` e compatíveis com o runtime remoto.
- Dados e modelos necessários disponíveis por caminhos relativos; nenhum segredo no código.
- Recursos devem respeitar os limites do plano utilizado.

## Testes e validações

- Validar localmente com instalação limpa antes do deploy.
- Conferir logs de build e ausência de exceções na inicialização.
- Testar a URL em janela anônima e em viewport desktop e móvel.
- Exercitar filtros, estados sem resultado, clusters e ao menos três previsões.

## Critérios mínimos de aceite

- A URL pública carrega sem autenticação e sem erro.
- Todas as funções essenciais operam com dados e modelo corretos.
- O link do README aponta para o app publicado.

## Tarefas de implementação

1. Concluir a auditoria do repositório da spec 002.
2. Criar ou acessar a conta do Streamlit Community Cloud.
3. Selecionar repositório, branch e `dashboard/app.py` para implantação.
4. Resolver erros de dependências, caminhos ou recursos apresentados nos logs.
5. Executar os testes funcionais na URL pública.
6. Inserir a URL validada no README e publicar a alteração.
7. Registrar evidência do deploy para a apresentação.
