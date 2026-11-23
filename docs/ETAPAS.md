# Guia de execução — Projeto Axes (passo a passo)

## Passo 0 — Proteger seu trabalho anterior

- [ ] **Não excluir** os exercícios dos Módulos 1–3.
- [ ] Fazer uma cópia da pasta antiga `Projeto-Axes` fora do repositório que será publicado.
- [ ] Se quiser preservar o CSV mais recente da pasta antiga, copiar **com backup** o conteúdo de `dados/cadastro_teste.csv` para o novo `dados/departamentos.csv` (somente depois de confirmar o cabeçalho `nome,contratacoes,meta`). **Não sobrescrever seus dados sem conferir.**
- [ ] Criar uma pasta nova (por exemplo, `Projeto-Axes-Portfolio`) e extrair a entrega nela. Assim você testa sem quebrar a versão antiga.

## Parte 1 — Finalização da fundação (v0.1)

### 1. Abrir no VS Code

- [ ] Arquivo > Abrir Pasta > escolher a **nova pasta extraída**.
- [ ] Abrir Terminal > Novo Terminal.
- [ ] Executar `python --version` e confirmar Python 3.11+; se `python` não funcionar, tente `py -3.11` no Windows.

### 2. Conferir a estrutura e os dados

- [ ] Verificar presença de `axes.py`, `axes_core.py`, `dados/departamentos.csv`, `tests`, `.gitignore`, `README.md`.
- [ ] **Não apagar** `exercicios/` se houver sido copiada do projeto antigo; ela documenta seu aprendizado.
- [ ] Arquivar `axes_backup.py`, `departamentos.txt`, `novo_relatorio.csv` e outros testes antigos **fora da pasta que vai para o Git**, se não forem usados. Não apagar sem conferir o conteúdo.

### 3. Executar e testar no terminal

- [ ] `python axes.py` abre o menu.
- [ ] Escolher `3`: gera relatório com RH, TI e MARKETING.
- [ ] Escolher `1`: cadastrar PESQUISA com 7 de 10; relatório deve exibir 70% imediatamente.
- [ ] Sair com `0`, executar novamente e confirmar persistência.
- [ ] Atualizar PESQUISA para 9 de 10 com confirmação `S`, conferir 90%.
- [ ] Testar cancelamento com `N` e confirmar que o CSV não mudou.
- [ ] Testar meta 0, meta negativa, contratações negativas e texto `abc`; o programa pede número válido sem encerrar.
- [ ] Remover PESQUISA respondendo `S`; executar novamente e confirmar ausência do registro.

### 4. Rodar testes automáticos

- [ ] Executar `python -m unittest discover -s tests -v`.
- [ ] Conferir que **6 testes** passaram (`OK`).
- [ ] Se ocorrer erro, guardar a saída e corrigir antes do commit.

### 5. Conferir o que entra no Git

- [ ] `git --version`.
- [ ] Se a pasta não tiver `.git`, executar `git init`; caso já tenha, **preservar o histórico**.
- [ ] `git status`.
- [ ] `git add .`.
- [ ] `git diff --cached --stat` e `git status` para revisar os arquivos preparados.
- [ ] Verificar que **nenhum dado pessoal real, senha, token, `axes_okr.db` ou backup** aparece na lista.
- [ ] `git commit -m "feat: primeira versao do Axes e estrutura inicial de OKRs"`.
- [ ] `git branch -M main` apenas se apropriado para o repositório.

### 6. Publicar no GitHub

- [ ] Criar repositório novo no GitHub; decidir **público ou privado**. Para portfólio, público com dados fictícios; se preferir estudar com privacidade, privado inicialmente.
- [ ] Criar repositório **sem** README, .gitignore e licença gerados automaticamente, pois estes já existem no projeto.
- [ ] Se ainda não houver remoto: `git remote add origin https://github.com/SEU_USUARIO/projeto-axes.git`.
- [ ] Se já houver remoto: `git remote -v` para conferir endereço e não duplicar `origin`.
- [ ] `git push -u origin main`.
- [ ] Abrir a página no GitHub e verificar que o README, o código e os testes estão visíveis; verificar que dados privados e arquivos locais não foram publicados.

**Conclusão da Parte 1:** consideramos concluída só quando o programa e os testes funcionarem **no seu computador**, os arquivos estiverem organizados e o GitHub exibir o commit. Até lá, publicação é pendente.

## Parte 2 — Primeiros cadastros de OKR Core

- [ ] Rodar `python okr.py`.
- [ ] Criar área fictícia.
- [ ] Criar colaborador fictício vinculado à área.
- [ ] Criar ciclo ano/trimestre.
- [ ] Criar objetivo com área e ciclo.
- [ ] Criar KR com valor inicial, meta, unidade e direção.
- [ ] Consultar os registros (opção `6`).
- [ ] Sair e reabrir; conferir que as informações ficaram no banco SQLite local.

**A Parte 2 desta entrega é um ponto de partida funcional, não uma plataforma empresarial pronta.** Ainda não temos edição e remoção de todas as entidades, histórico de check-ins, alertas, autenticação ou dashboards. Iremos desenvolver isso incrementalmente.

## Próximos passos depois da Parte 2

1. Histórico de check-ins por mês (sem sobrescrever resultados antigos).
2. Regras para KRs de aumento e redução; comparação entre ciclos.
3. Alertas simples de atraso, estagnação e check-in não realizado.
4. Dashboards com Streamlit/Plotly.
5. Agente de IA com consultas controladas sobre os resultados do motor.
6. Segurança para ambientes empresariais apenas após desenho de autenticação, papéis/permissões, auditoria, backups, isolamento por empresa e requisitos legais.
