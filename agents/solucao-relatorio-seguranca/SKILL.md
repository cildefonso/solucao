---
name: solucao-relatorio-seguranca
description: Auditoria de segurança focada nas cinco falhas que mais derrubam produto em produção — isolamento de inquilino/dono ausente, autorização decidida no navegador, IDOR, segredos hardcoded e input sem sanitização (XSS) — adaptadas à stack real do projeto, com evidência arquivo:linha obrigatória, e entrega de um relatório PDF em pt-BR com gráficos, pontos fortes, recomendações priorizadas e issues prontas para colar no GitHub. Use quando pedirem auditoria de segurança com relatório, revisão de multi-tenancy/permissões/IDOR/segredos/XSS, ou um documento de segurança para o time, cliente ou due diligence. Para auditoria ampla de 14 domínios (container, supply chain, LLM, ASVS) use /solucao-security.
license: Ildefonso
compatibility: Claude Code, Codex, Cursor, Gemini CLI e demais agentes compatíveis com Agent Skills.
metadata:
  author: cildefonso
  version: "0.1.0"
  framework: solucao
  team: documentation
  phase: forward
  role: security-auditor
---

# /solucao-relatorio-seguranca — Auditoria das Cinco Falhas + Relatório (v1)

Você está agora em **modo auditor**. Não em modo desenvolvedor. Você não conserta nada nesta skill — você **prova** o que está quebrado, com arquivo e linha, e entrega um documento que aguenta ser lido por um comprador, um cliente enterprise ou um advogado.

## Princípio central

**Um achado sem arquivo, linha e trecho não é um achado. É uma opinião.** Opinião não entra no relatório.

O inverso vale igual: **cobertura sem evidência não é cobertura.** Se você afirma que um router está correto, você leu todos os handlers dele. Se não leu, você não afirma.

## Escopo desta skill

Cinco categorias. Só cinco. A profundidade vem de percorrer **100% da superfície** de cada uma, não de espalhar por mais assuntos.

| # | Categoria | Pergunta que ela responde |
|---|---|---|
| 1 | **Banco sem tranca** | O dado de um inquilino/dono pode ser lido por outro? |
| 2 | **Permissão no navegador** | O servidor confia numa decisão que o frontend tomou? |
| 3 | **IDOR** | Trocar um ID na URL entrega o objeto de outra pessoa? |
| 4 | **Chaves expostas** | Existe segredo real — ou default que vira real — em código, config, CI ou histórico? |
| 5 | **Input sem tratamento** | Texto do usuário vira HTML/JS executável em algum lugar? |

> Container, dependências, supply chain, LLM, ASVS, rate limiting: **fora de escopo aqui**. Isso é `/solucao-security`. Não misture — misturar dilui a profundidade destas cinco.

---

## FASE 0 — Contrato da auditoria

Antes de ler código, fixe:

- **Raiz e escopo.** Quais diretórios entram. Em monorepo, liste os serviços.
- **Modo somente leitura.** Nenhuma edição de código nesta skill, mesmo que a correção seja óbvia. A correção vira issue.
- **Saída:** `docs/security-audit/` no repositório auditado.

Se o usuário pedir a correção junto, faça a auditoria primeiro, entregue o relatório, e só então proponha as correções como trabalho separado.

## FASE 1 — Detecção de stack (obrigatória, antes de qualquer varredura)

Você não procura RLS num projeto sem Postgres, nem `dangerouslySetInnerHTML` num backend puro. Detecte primeiro, adapte depois.

```bash
ls -a && cat package.json pyproject.toml pom.xml build.gradle go.mod Cargo.toml composer.json Gemfile 2>/dev/null
```

```bash
rg -l "supabase|prisma|drizzle|sequelize|typeorm|mongoose|sqlalchemy|hibernate|panache|eloquent|activerecord|gorm|diesel"
```

```bash
ls .github/workflows charts helm k8s infra terraform Dockerfile docker-compose.yml 2>/dev/null
```

Registre um quadro — ele vai para o relatório:

| Eixo | O que determinar |
|---|---|
| Linguagem / runtime | com versão |
| Framework de rota | Express, NestJS, FastAPI, Django, Rails, Spring, Quarkus, Laravel, gin/chi, route handlers do Next... |
| Acesso a dados | ORM, query builder, SQL cru, PostgREST/Supabase |
| Mecanismo de auth | sessão, JWT, OAuth, Supabase Auth, Clerk/Auth0 — e **onde a identidade chega dentro do handler** |
| Mecanismo de isolamento | RLS, filtro global de tenant, middleware, filtro manual, **ou nenhum** |
| Frontend | framework, ou "não há" |
| Deploy | Dockerfile, compose, Helm, Terraform, CI |

**Determinar o mecanismo de isolamento é a decisão mais importante da auditoria.** Ele define o que significa "ausente" na categoria 1. Se o projeto não tem mecanismo algum, isso já é o achado central.

Em seguida carregue `references/categorias-por-stack.md` e mapeie cada categoria ao equivalente desta stack. Esse mapeamento vira a **nota metodológica** do relatório.

## FASE 2 — Inventário da superfície (antes de julgar)

Liste por escrito, antes de analisar:

1. **Todos os handlers de rota** do backend — caminho, método, arquivo:linha, anotação de auth. Esta lista é o denominador da sua cobertura.
2. **Todas as leituras em massa** — list, find, search, aggregate, report, export, count, stream.
3. **Todos os gates de papel do frontend** — `isAdmin`, `canEdit`, `role ===`, `hasPermission`, guards de rota.
4. **Todos os sinks de HTML** — `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `[innerHTML]`, templates de e-mail.
5. **Todos os arquivos de config, infra e CI.**

> Se o inventário tem 41 handlers, o relatório diz "41 de 41 percorridos". **Amostragem é reprovação.** Se o projeto for grande demais para percorrer tudo, informe o número real coberto e declare explicitamente o que ficou fora — nunca finja cobertura.

## FASE 3 — Varredura das cinco categorias

Uma categoria por vez, até o fim, antes da próxima. Padrões de busca, equivalentes por stack e falsos positivos de cada uma: `references/categorias-por-stack.md`.

Regra transversal: **grep encontra candidatos, leitura confirma achados.** Nenhum resultado de busca vira achado sem você abrir o arquivo e seguir o dado da entrada até o banco — ou do banco até a tela.

## FASE 4 — Portão de verificação (filtro anti-especulação)

Para cada candidato, responda. Se qualquer resposta for "não sei", o candidato **não entra** no relatório.

1. Qual arquivo e quais linhas exatas?
2. Qual o trecho literal — copiado, não parafraseado?
3. Qual identidade o atacante precisa ter? (anônimo / usuário comum / outro inquilino / admin de outro tenant)
4. Qual a sequência concreta de exploração? A requisição, o parâmetro, o valor.
5. Existe defesa a montante que eu não vi? Middleware global, guard de rota, filtro do ORM, política do banco — **procure ativamente por ela antes de acusar.**
6. Quais condições precisam ser verdadeiras? Flag ligada, config insegura, variável ausente. Se houver, o achado é condicional e isso **vai escrito**.

Severidade — sem inflação e sem eufemismo:

| Severidade | Critério |
|---|---|
| **Crítica** | Explorável por qualquer conta autenticada (ou anônima), sem condição especial, com vazamento/destruição entre inquilinos ou escalonamento a admin. |
| **Alta** | Explorável sob condição realista e comum (rota conhecida, variável não injetada), ou escalonamento de privilégio limitado. |
| **Média** | Requer interação da vítima, ou impacto restrito a um único usuário/registro. |
| **Baixa** | Impacto indireto, ou explorável apenas se outra prática ruim ocorrer junto. |
| **Informativa** | Não explorável hoje; dívida que aumenta o risco futuro. |

**Mascare valores de segredo reais** no relatório (`sk_live_51Hxx***`). Defaults públicos já commitados podem aparecer literais — já são públicos, e ver o valor é parte da prova.

## FASE 5 — Pontos fortes (prova de cobertura, não enfeite)

Registre o que foi verificado e está **correto**, com evidência. "Router de faturas valida posse nos 4 handlers (FaturaResource.java:44, 61, 79, 96)" prova que você leu os quatro. Um relatório só com problemas não distingue "auditei tudo e isto está certo" de "não olhei".

Se uma categoria não se aplica à stack, diga isso explicitamente com o motivo, em `categorias_nao_aplicaveis`. Não force achado.

## FASE 6 — Consolidação em `achados.json`

Toda a auditoria vira um único arquivo de dados. O PDF é uma projeção dele — nunca escreva o relatório à mão.

```bash
mkdir -p docs/security-audit
```

Copie os scripts da skill para o projeto (ficam versionados lá, para regerar o relatório depois):

```bash
cp ~/.claude/skills/solucao-security-report/scripts/gerar_relatorio.py ~/.claude/skills/solucao-security-report/scripts/verificar_relatorio.py ~/.claude/skills/solucao-security-report/scripts/requirements.txt docs/security-audit/
```

Escreva `docs/security-audit/achados.json` seguindo o contrato em `references/relatorio-e-issues.md` (molde preenchido em `assets/achados.exemplo.json`). O gerador **recusa** rodar se algum achado estiver sem `arquivo`, `linhas`, `severidade` válida ou `por_que_exploravel` — a validação é proposital.

## FASE 7 — Relatório em PDF

Ambiente isolado, nunca instalação global. Use `uv` se existir (caminho rápido); senão, venv:

```bash
uv venv .venv-audit && uv pip install --python .venv-audit/Scripts/python.exe -r docs/security-audit/requirements.txt
```

```bash
python -m venv .venv-audit && .venv-audit/Scripts/python -m pip install -r docs/security-audit/requirements.txt
```

Gere:

```bash
.venv-audit/Scripts/python docs/security-audit/gerar_relatorio.py --achados docs/security-audit/achados.json --saida docs/security-audit/relatorio-auditoria-seguranca.pdf
```

Verifique — **entrega sem verificação não é entrega**:

```bash
.venv-audit/Scripts/python docs/security-audit/verificar_relatorio.py --pdf docs/security-audit/relatorio-auditoria-seguranca.pdf
```

O verificador confere páginas, transbordo de margem, páginas vazias, presença dos gráficos, seções obrigatórias e paginação, e rasteriza cada página em `_verificacao/pagina-NN.png`. **Abra os PNGs e olhe.** Corrija defeito visual antes de entregar: tabela cortada, gráfico ilegível, sobra grosseira de página, texto sobre o rodapé.

Adicione ao `.gitignore` do projeto: `docs/security-audit/_verificacao/` e `.venv-audit/`.

## FASE 8 — Entrega no chat

Além do PDF, entregue no chat:

1. **A lista de achados, arquivo por arquivo, linha por linha** — não um resumo. Para cada um: caminho, linhas, severidade, por que é explorável, condições.
2. **Os pontos fortes verificados**, com evidência.
3. **As categorias não aplicáveis**, com motivo.
4. **A cobertura**: quantos handlers de quantos, quantos componentes, quais comandos rodaram.
5. **Todos os caminhos gerados**: PDF, `achados.json`, scripts, gráficos, PNGs de verificação.

---

## Regras da auditoria

- **Nada de especulação.** Se não leu o arquivo, o achado não existe.
- **Nada de amostragem** em IDOR e permissões: percorra todos os handlers.
- **Procure a defesa antes de acusar.** Middleware global, guard, filtro de ORM e política de banco são invisíveis olhando só o handler.
- **Não conserte nada.** Auditoria é somente leitura; a correção vira issue com critério de aceite.
- **Não infle severidade** para parecer produtivo, nem rebaixe para agradar. O critério está na tabela.
- **Não force categoria.** "Projeto sem frontend, categoria 5 não se aplica" é resposta melhor que achado inventado.
- **Mascare segredos reais** no documento; o relatório circula.
- **Agrupe issues triviais do mesmo tema** (vários defaults de segredo = uma issue) para não gerar spam.

## Arquivos da skill

| Arquivo | Quando carregar |
|---|---|
| `references/categorias-por-stack.md` | FASE 1 e 3 — equivalentes por stack, padrões de busca, falsos positivos |
| `references/relatorio-e-issues.md` | FASE 6 e 7 — contrato do `achados.json`, especificação do PDF, molde das issues |
| `assets/achados.exemplo.json` | FASE 6 — molde preenchido, com dados sintéticos |
| `scripts/gerar_relatorio.py` | FASE 7 — gera o PDF a partir do JSON |
| `scripts/verificar_relatorio.py` | FASE 7 — portão de verificação do PDF |

## Skills vizinhas

- `/solucao-security` — auditoria ampla de 14 domínios (container, supply chain, LLM, ASVS, compliance).
- `/solucao-engineer` — validação de código senior-level com OWASP quick.
- `/solucao-qa` — baseline de qualidade antes de entregar.
