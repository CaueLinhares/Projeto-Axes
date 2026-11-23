# Projeto Axes

**Do portfólio ao protótipo de uma plataforma de OKRs.** Este repositório de estudos usa dados fictícios e duas aplicações separadas, ambas em Python 3.11+:

- **Parte 1 — Axes v0.1 (`axes.py`)**: cadastro, edição, remoção, relatório de atingimento e persistência em CSV.
- **Parte 2 — OKR Core inicial (`okr.py`)**: cadastro de áreas, colaboradores fictícios, ciclos, objetivos e resultados-chave (KRs) em SQLite.


**Situação:** a Parte 1 — Axes v0.1 foi validada localmente, com 6 testes automatizados aprovados, e publicada no GitHub.

A Parte 2 — OKR Core está em desenvolvimento, com os primeiros cadastros em SQLite. Histórico mensal, alertas, dashboards, permissões e agente de IA serão implementados nas próximas versões.


## Requisitos

- Windows, macOS ou Linux
- Python **3.11 ou superior**
- VS Code e extensão Python (recomendados)
- Git instalado para versionamento/publicação
- **Sem dependências externas**: usa apenas a biblioteca padrão (`csv`, `pathlib`, `sqlite3`, `unittest`).

## Estrutura

```text
Projeto-Axes/
├── axes.py                   # Menu da Parte 1 (terminal)
├── axes_core.py              # Regras e persistência CSV
├── okr.py                    # Menu da Parte 2 (terminal)
├── okr_core.py               # Regras e persistência SQLite
├── dados/
│   └── departamentos.csv     # Exemplo fictício da Parte 1
├── tests/
│   ├── test_axes_core.py
│   └── test_okr_core.py
├── docs/
│   └── ETAPAS.md
├── .gitignore
└── README.md
```

## Como rodar

Abra a **pasta inteira do projeto** no VS Code (Arquivo > Abrir Pasta). No terminal, confira:

```powershell
python --version
```

### Parte 1 — Sistema básico

```powershell
python axes.py
```

Opções: **1** cadastrar/atualizar, **2** remover com confirmação, **3** relatório, **0** sair.

Exemplo: cadastre o departamento `PESQUISA`, com `7` contratações e meta `10`. O relatório exibirá 70%. Saia, abra o programa de novo e confirme que PESQUISA continua lá. Para atualizar, repita o nome, responda `S` e digite os novos números.

Os dados reais deste programa estão em `dados/departamentos.csv`. A função de salvamento primeiro escreve em um arquivo temporário e depois substitui o CSV, reduzindo o risco de deixar o arquivo pela metade em caso de falha.

### Parte 2 — OKR Core (primeiro protótipo)

```powershell
python okr.py
```

No menu, siga **esta ordem**:

1. Cadastrar uma **área** (ex.: PESSOAS E CULTURA). Guarde o ID exibido.
2. Cadastrar um **colaborador fictício** e informar o ID da área.
3. Cadastrar um **ciclo**, por exemplo **2027, trimestre 1**.
4. Cadastrar um **objetivo**, informando IDs de área e ciclo.
5. Cadastrar um **KR**, informando o ID do objetivo, linha de base, meta, unidade e direção (`aumentar`/`diminuir`).
6. Consultar os registros pela opção **6**.

Exemplo fictício de KR: *Reduzir o tempo médio de contratação de 45 para 30 dias*. Valores: **45** (início), **30** (meta), **dias** (unidade), **diminuir** (direção).

Esse programa cria automaticamente `dados/axes_okr.db`, que **não será enviado ao Git** porque o `.gitignore` ignora bancos locais. Há validações básicas e relacionamento entre tabelas, mas não há ainda interface web ou gestão completa de OKRs.

## Testes automatizados

```powershell
python -m unittest discover -s tests -v
```

Resultado esperado nesta entrega: **6 testes** passando com `OK`. Os testes cobrem cálculo, duplicidade, atualização, remoção, persistência CSV, cadastro de entidades OKR e algumas entradas inválidas. Isso é uma base de testes, **não** um selo de segurança ou qualidade de produção.

## Git e GitHub

Antes de publicar, leia **[docs/ETAPAS.md](docs/ETAPAS.md)**. Resumo:

```powershell
git --version
git init
git status
git add .
git diff --cached --stat
git commit -m "feat: estrutura inicial do Axes com CSV e OKR Core"
git branch -M main
```

Depois de criar um repositório vazio no GitHub (sem README automático), conecte o remoto. **Substitua `SEU_USUARIO` pelo seu usuário**, e escolha se o repositório será público ou privado:

```powershell
git remote add origin https://github.com/SEU_USUARIO/projeto-axes.git
git push -u origin main
```

**Se o seu projeto já tem um repositório Git**, **não** execute `git init` ou `git remote add origin` às cegas: primeiro confira `git status` e `git remote -v`; mantenha o histórico existente.

## Escopo e segurança

- Usar **somente dados fictícios**, especialmente nas demonstrações públicas.
- Não colocar dados corporativos, senhas, chaves, arquivos `.env` ou bancos locais no repositório.
- O uso atual é individual e local. **Não** há login, permissão por área, auditoria, criptografia de banco nem isolamento entre empresas. **Não é adequado à produção empresarial**.
- A evolução sugerida inclui histórico de check-ins, comparação temporal, alertas, dashboard e agente de IA com acesso controlado.

## Próxima evolução

Após validar a Parte 1 e o protótipo da Parte 2, construiremos o histórico mensal de check-ins. Esse histórico será indispensável para medir a evolução dos KRs sem apagar períodos anteriores.
