---
name: solucao-auditoria-codigo
description: 'Auditoria de segurança estática e somente leitura focada em 5 categorias críticas: Banco Sem Tranca (isolamento de inquilino/dono), Permissão Definida no Navegador, IDOR, Chaves Expostas e Inputs Sem Tratamento (XSS/injeção em saída). Produz findings.json, relatório PDF pt-BR com gráficos, matriz de cobertura e issues prontas para o GitHub. Pode auditar o repositório inteiro ou apenas uma funcionalidade (modo funcionalidade), gravando o relatório na pasta da funcionalidade. É chamada pela skill solucao-angular-incremental-frontend após o código ser criado.'
argument-hint: 'Opcional: caminho do repositório ou da pasta da funcionalidade a auditar, e pasta de saída (padrão: repositório atual e docs/security-audit/)'
user-invocable: true
---

# Auditoria de Segurança — 5 categorias críticas

Você vai fazer uma auditoria de segurança estática e somente leitura deste repositório, focada em cinco categorias de falha. O objetivo é produzir achados verificados, reproduzíveis e acionáveis, com prova de cobertura, além de um relatório em PDF e issues prontas para o GitHub.

## PARÂMETROS DE EXECUÇÃO — escopo e pasta de saída

Antes de começar, defina o **modo**, o **escopo** e a **`<PASTA_SAIDA>`**. Em todo este documento, `<PASTA_SAIDA>` substitui a pasta de entregáveis.

| Modo | Quando | Escopo auditado | `<PASTA_SAIDA>` |
|---|---|---|---|
| **Repositório** (padrão) | Invocação direta pelo usuário sem indicar funcionalidade | Repositório inteiro | `docs/security-audit/` |
| **Funcionalidade** | Chamada por outra skill (ex.: `solucao-angular-incremental-frontend`) ou usuário indica uma funcionalidade | Arquivos criados/alterados pela funcionalidade (pasta da feature, serviços, modelos, rotas, guards, navegação, traduções, ambientes) **e** os endpoints de backend que ela consome, quando o path do backend foi informado | `<pasta da funcionalidade>/security-audit/` (ex.: `src/app/features/<feature>/security-audit/`) |

Regras do modo funcionalidade:
- A lista de arquivos do escopo vem de quem chamou a skill (a skill chamadora deve repassá-la) ou de `git status`/`git diff` contra a branch base. Registre essa lista no `findings.json` (`metadados.escopo`) e na capa do PDF.
- O inventário de pontos de entrada (1.2) e a matriz de cobertura cobrem os pontos de entrada **da funcionalidade**: rotas Angular e seus guards, chamadas HTTP do serviço da feature e os handlers backend correspondentes (resource/controller). Ainda assim, leia o contexto necessário fora do escopo (interceptors, guards globais, configuração de autenticação, ambientes, `.gitignore`) para validar os achados, e declare como "fora do escopo" o restante do repositório.
- O venv **não** pode ficar dentro de `src/` nem de qualquer pasta incluída no build/lint/testes: use um diretório temporário fora do repositório (ex.: diretório temporário do sistema ou scratchpad da sessão). Os demais entregáveis vão para `<PASTA_SAIDA>`.
- Se o projeto tiver ferramentas que varrem `src/` (tsconfig `include`, ESLint, Karma, Sonar), confira que `<PASTA_SAIDA>` não quebra build, lint nem testes (ela só contém `.json`, `.md`, `.pdf`, `.py`, `.txt` e `.png`); se quebrar, informe a quem chamou e proponha a exclusão adequada.
- A auditoria não corrige código. Os achados são devolvidos à skill chamadora, que decide com o usuário o que corrigir.

Em ambos os modos, considere a pasta de saída como a única área onde é permitido gravar arquivos.

## 0. REGRAS INVIOLÁVEIS

- Não altere código da aplicação. Você só pode criar arquivos dentro de `<PASTA_SAIDA>` (e um venv fora do repo ou em `<PASTA_SAIDA>/.venv` — apenas no modo repositório —, que deve ser adicionado ao `.gitignore` local da pasta).
- Não execute exploits contra ambientes reais, não faça requisições a URLs de produção/staging encontradas no código e não use credenciais encontradas para testar acesso.
- Nunca reproduza um segredo completo no chat, no PDF, nos arquivos gerados ou nas issues. Mascare sempre: mostre só o tipo, os 4 primeiros caracteres e o tamanho (ex: `sk_live_51Hx…` → `sk_l…(107 chars)`). Issues podem ir para repositórios públicos.
- Só reporte o que foi verificado no código real. Cada achado precisa de arquivo, linha(s), trecho e cadeia de exploração concreta. Se algo depende de comportamento em runtime que você não conseguiu confirmar, classifique como **Confiança: provável** e diga exatamente o que falta confirmar — nunca apresente suposição como fato.
- Cobertura sistemática, não amostragem. Quando a instrução disser "todos", são todos. Se o repositório (ou o escopo) for grande demais para cobrir integralmente, declare explicitamente o que ficou de fora e por quê, em vez de dar a entender cobertura total.
- Instale dependências apenas em ambiente isolado (venv Python, `npx` sem `-g`, binário baixado para pasta temporária). Nada global.

## 1. FASE DE RECONHECIMENTO (obrigatória antes de qualquer achado)

Produza, e registre no relatório, um mapa da stack e da superfície de ataque:

### 1.1 Stack

- Linguagem(ns) e versões; framework(s) backend e frontend; monorepo/workspaces.
- ORM / query builder / SQL cru; banco(s); cache; filas; storage de arquivos; busca (Elastic, Algolia, pgvector…).
- Mecanismo de autenticação (sessão, JWT próprio, Supabase Auth, Auth0, Clerk, NextAuth, Firebase…) e onde a identidade do usuário é extraída em cada requisição.
- Modelo de autorização: papéis, permissões, multi-tenant (organização/workspace/conta/time), e qual é o mecanismo de isolamento (RLS, middleware de tenant, escopo global do ORM, filtro manual por `user_id`/`org_id`, schema-por-tenant, banco-por-tenant).
- Deploy e infra: Dockerfile, docker-compose, CI/CD, Helm, Terraform, Vercel/Netlify/Fly, edge functions, serverless.
- Se o projeto integra LLMs: onde a saída do modelo é renderizada e quais ferramentas/ações o modelo pode disparar.

### 1.2 Inventário de pontos de entrada

Liste todos os pontos de entrada que recebem input externo, com `arquivo:linha`:

- Rotas HTTP/REST, resolvers GraphQL (queries, mutations, subscriptions, field resolvers), tRPC/RPC, Server Actions, API routes, route handlers.
- WebSockets / Realtime / SSE.
- Webhooks recebidos (Stripe, GitHub, etc.).
- Edge/serverless functions, Supabase Edge Functions, funções Postgres expostas via RPC.
- Jobs, workers, cron e consumidores de fila que processam dados vindos de usuários.
- Upload/download de arquivos, URLs assinadas.

Esse inventário vira a matriz de cobertura (seção 4.3). Todo ponto de entrada deve aparecer nela com o resultado da verificação para as categorias 1, 2 e 3.

## 2. AS CINCO CATEGORIAS

Para cada categoria, adapte à stack detectada. Se não se aplicar (ex: projeto sem frontend), diga explicitamente e explique por quê.

### Categoria 1 — BANCO SEM TRANCA (isolamento de inquilino/dono)

Identifique o mecanismo de isolamento e procure onde ele está ausente, furado ou contornado.

**Se Supabase/Postgres com RLS:**

- Tabelas em schemas expostos (`public` e outros em `db_schemas`) sem `ENABLE ROW LEVEL SECURITY`. Revise todas as migrations, não só a mais recente (uma migration posterior pode desabilitar RLS ou recriar a tabela).
- Políticas permissivas: `USING (true)`, `TO public`/`anon` onde não deveria, políticas que confiam em coluna editável pelo próprio usuário.
- `UPDATE`/`INSERT` sem `WITH CHECK` (permite mover uma linha para outro dono/tenant).
- Operações sem política correspondente (ex: há `SELECT` mas `DELETE` cai em política genérica).
- Políticas baseadas em `auth.jwt() -> 'user_metadata'` — `user_metadata` é editável pelo próprio usuário; papel/tenant deve vir de `app_metadata` ou tabela controlada pelo servidor.
- Views sem `security_invoker = true` (ignoram RLS da tabela base), funções `SECURITY DEFINER` sem checagem interna de posse e sem `search_path` fixo, funções expostas via RPC.
- Policies de Storage (`storage.objects`) e de Realtime.
- Uso de `service_role` key: onde é usada, se alguma rota a usa para atender requisição de usuário sem refazer o filtro manualmente, e se ela vaza para o cliente.

**Se API própria (ORM/SQL):**

- Queries de listagem, busca, contagem, agregação, relatório, exportação (CSV/XLSX/PDF), dashboard e autocomplete sem filtro por usuário/tenant.
- Escopo global do ORM que existe mas é contornado (`unscoped`, `withoutGlobalScope`, `$queryRaw`, SQL cru, `knex.raw`).
- Middleware de tenant que não cobre todas as rotas (matcher incompleto, rotas registradas antes do middleware, rotas de outra versão da API).
- Tenant/org ID lido do body, query ou header controlado pelo cliente em vez da sessão.
- Jobs/workers que processam dados sem contexto de tenant.
- Caches, chaves de Redis, índices de busca e vetoriais (embeddings/RAG) sem segregação por tenant — em apps de LLM, verifique se a recuperação de contexto filtra por dono.
- Caminhos de arquivos em storage previsíveis e não vinculados ao tenant.

### Categoria 2 — PERMISSÃO DEFINIDA NO NAVEGADOR

- Mapeie todo gate de papel no frontend (`isAdmin`, `canEdit`, `role ===`, `hasPermission`, rotas protegidas, menus condicionais, feature flags no cliente) e cruze cada um com o endpoint que ele protege. Para cada par, confirme se o backend faz a verificação equivalente. Registre os pares corretos também.
- Rotas/ações sensíveis sem checagem de papel no servidor: admin, configurações, billing, convites, gestão de membros/papéis, exclusões em massa, exportações, impersonação.
- Mass assignment: endpoints de update/cadastro que aceitam o objeto inteiro do body e permitem setar `role`, `is_admin`, `org_id`, `owner_id`, `plan`, `credits`, `verified`, `status`.
- Confiança em dados do cliente: papel vindo de `localStorage`, cookie não assinado, header customizado, claim de JWT não verificado (`jwt.decode` sem verify, `alg: none`, segredo fraco), `user_metadata`.
- Server Actions/tRPC/GraphQL mutations expostas sem checagem (o fato de não haver botão na UI não impede a chamada).
- Divergência de método (GET protegido, POST/PUT/PATCH/DELETE da mesma rota não).
- Escalada horizontal de papel: um admin de tenant A conseguindo agir no tenant B.

### Categoria 3 — IDOR

Percorra todos os handlers do inventário que recebem um identificador (path, query, body, header, nome de arquivo, ID de nó GraphQL, canal de WebSocket) e verifique se há checagem de posse/tenant antes de ler, alterar ou excluir. Atenção a:

- Recursos aninhados (`/orgs/:orgId/projects/:projectId`) que validam o `orgId` mas não verificam se o `projectId` pertence a ele.
- Endpoints em lote (`ids: [...]`) que validam só o primeiro item ou nenhum.
- Updates que permitem trocar a FK (`project_id`, `org_id`) para mover o objeto para outro tenant.
- Download de arquivo, geração de URL assinada, anexos, avatares, exports.
- Subscriptions/realtime/canais por ID.
- Objetos com soft delete ou arquivados ainda acessíveis.
- UUID não é controle de acesso: registre o IDOR mesmo com UUID, ajustando a severidade conforme a facilidade de obter/vazar o ID (aparece em URLs compartilhadas, logs, respostas de outros endpoints?).

### Categoria 4 — CHAVES EXPOSTAS

Procure em código, configs, `.env*` versionados, docker-compose, Dockerfile (`ENV`, `ARG`), charts Helm, Terraform (`*.tfvars`, state), CI (`.github/workflows`, GitLab CI), scripts, notebooks, fixtures de teste, seeds, documentação e README:

- API keys, tokens, senhas, connection strings com senha, segredos de assinatura (JWT, sessão, webhooks, cookies), chaves privadas (PEM, SSH), credenciais de cloud.
- Defaults públicos que viram segredo real (`${VAR:-valor}`, `os.getenv("X", "changeme")`, `process.env.X || "secret"`) e ausência de validação no startup que rejeite esses defaults em produção.
- Credenciais padrão de serviços (Postgres `postgres/postgres`, MinIO, Redis sem senha, painéis admin).
- Frontend/bundle: variáveis com prefixo público (`NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`, `EXPO_PUBLIC_`, `PUBLIC_`) contendo segredo; source maps publicados; chaves em apps mobile. Se houver build pronto (`dist/`, `.next/`, `build/`), faça grep nele; se não houver, analise estaticamente o que entraria no bundle (no Angular, inclua `src/environments/*.ts`).
- Diferencie chaves públicas por design (Supabase anon, Stripe `pk_`, Firebase config, Google Maps com restrição) — classifique como informativa, mas confirme que a segurança não depende delas — de chaves privilegiadas (`service_role`, `sk_live`, AWS secret), que são críticas.
- Histórico git: busque segredos já removidos do HEAD mas presentes em commits antigos (`git log -p --all`, `git log --all --diff-filter=D`). Se disponível sem instalação global, use gitleaks ou trufflehog em binário local; caso contrário, regex direcionadas (`AKIA`, `sk_live_`, `ghp_`, `xox[bp]-`, `-----BEGIN .*PRIVATE KEY`, `eyJ` longos, `service_role`, `password\s*[:=]`). No modo funcionalidade, restrinja o histórico aos arquivos do escopo.
- Para cada segredo, indique se continua no HEAD, só no histórico, e se parece real ou placeholder. A recomendação deve sempre incluir rotação, não só remoção.
- Verifique `.gitignore` (cobre `.env`, chaves, `*.pem`, `tfstate`?) e se segredos aparecem em logs (`console.log(process.env)`, log de headers de autorização).

### Categoria 5 — INPUTS SEM TRATAMENTO (XSS e injeção em saída)

**Frontend:**

- `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `dangerouslySetInnerHTML`, `v-html`, `[innerHTML]`/`bypassSecurityTrust*`, `{@html}` (Svelte), `$sce.trustAsHtml`, jQuery `.html()`/`$(userInput)`.
- Renderização de Markdown/HTML sem sanitização (marked, markdown-it com `html: true`, react-markdown com rehype-raw, remark-html sem sanitize).
- Saída de LLM renderizada como HTML/Markdown: trate como input não confiável (prompt injection → XSS, links/imagens que exfiltram dados via URL).
- URLs controladas pelo usuário em `href`, `src`, `action`, `formaction`, `window.location`, `window.open` sem bloquear `javascript:`/`data:`.
- `eval`, `new Function`, `setTimeout(string)`, templates compilados em runtime.
- `postMessage` sem validação de origin; JSON de estado embutido em `<script>` sem escape de `</script>`.
- Uploads de SVG/HTML servidos no mesmo domínio ou com Content-Type controlado pelo usuário.

**Backend:**

- Input do usuário em HTML de e-mails, templates (Jinja `|safe`/autoescape false, Handlebars `{{{ }}}`, EJS `<%-`, Blade `{!! !!}`), PDFs gerados a partir de HTML e respostas `text/html`.
- Respostas de erro que refletem input sem escape.

**Defesas a verificar (registrar como ponto forte ou fraco):**

- Lib de sanitização no projeto (DOMPurify, sanitize-html, bleach, rehype-sanitize) e se ela é de fato aplicada em cada ponto encontrado, com configuração segura.
- Cabeçalho CSP (e se usa `unsafe-inline`/`unsafe-eval`), cookies de sessão com `HttpOnly`/`Secure`/`SameSite`, tokens em `localStorage` (amplia o impacto de XSS).

## 3. CLASSIFICAÇÃO

### Severidade (use estes critérios, não intuição)

- **Crítica:** explorável remotamente por usuário não autenticado ou por qualquer usuário autenticado, com acesso/alteração de dados de outros tenants em massa, tomada de conta, ou segredo privilegiado ativo exposto.
- **Alta:** explorável por usuário autenticado comum contra dados ou ações de outros usuários/tenants, ou escalada para admin; XSS armazenado.
- **Média:** exige condição adicional (ID difícil de obter, interação da vítima, config não padrão, feature flag), ou impacto limitado; XSS refletido.
- **Baixa:** defesa em profundidade ausente, impacto mínimo ou exploração muito improvável.
- **Informativa:** boa prática, chave pública por design, observação sem risco direto.

### Para cada achado registre

- ID (`SEC-001`…), categoria, severidade, confiança (confirmado / provável).
- Arquivo e linha(s) exatas; trecho de código (máx. ~15 linhas, segredos mascarados).
- Cadeia de exploração: quem é o atacante, pré-requisitos, passos (ex: "usuário autenticado do tenant A faz `GET /api/invoices/123` com ID do tenant B").
- Condições de explorabilidade (feature flag, variável de ambiente, config insegura, rota só ativa em dev).
- Impacto (confidencialidade, integridade, disponibilidade; dados afetados).
- Causa raiz. Se vários achados têm a mesma causa (ex: middleware de tenant não aplicado a um router inteiro), agrupe sob a causa raiz e liste as ocorrências, em vez de inflar a contagem.
- Correção sugerida, específica para a stack.

### Fora do escopo

Se durante a varredura você notar falhas graves de outras categorias (SQL injection, SSRF, CSRF, path traversal, rate limiting ausente em login, deserialização insegura), registre-as brevemente numa seção "Observações fora do escopo", sem aprofundar e sem incluí-las na contagem principal.

## 4. ENTREGÁVEIS

Tudo em `<PASTA_SAIDA>`:

### 4.1 `findings.json` — fonte única da verdade

Todos os achados, pontos fortes, matriz de cobertura, inventário e metadados (projeto, data, commit SHA auditado, escopo, modo de execução). O gerador do PDF e das issues lê deste arquivo, para que o relatório possa ser regerado após correções.

### 4.2 Relatório `relatorio-auditoria-seguranca.pdf` (pt-BR, visualmente amigável)

- a) **Capa:** "Relatório de Auditoria de Segurança — <nome do projeto>" (no modo funcionalidade: "— <nome do projeto> / <funcionalidade>"), data, commit SHA, escopo auditado (diretórios incluídos/excluídos) e nota metodológica (como cada categoria foi mapeada para a stack detectada, ferramentas usadas e limitações da análise estática).
- b) **Sumário** com números de página.
- c) **Resumo executivo:** total de achados por severidade, gráfico de rosca por severidade, gráfico de barras empilhadas por categoria × severidade, e um parágrafo em linguagem não técnica com os 3 riscos principais. Paleta: crítica `#B91C1C`, alta `#EA580C`, média `#D97706`, baixa `#2563EB`, informativa `#6B7280`, ponto forte `#059669`.
- d) **Stack e superfície de ataque:** resumo da fase de reconhecimento.
- e) **Pontos fortes** (o que está protegido, com evidência `arquivo:linha`) e **pontos fracos** (riscos centrais e causas raiz).
- f) **Achados detalhados por categoria:** tabela ID | Severidade | Confiança | Arquivo:linha | Descrição, com chip de severidade colorido, seguida do detalhamento de cada achado (trecho de código em fonte monoespaçada, exploração, impacto, correção).
- g) **Matriz de cobertura:** cada ponto de entrada × categorias 1/2/3 com status (✔ protegido / ✘ achado / — não se aplica), provando que nada foi pulado. Pode ir em apêndice.
- h) **Recomendações priorizadas:** P1 (corrigir imediatamente, inclui rotação de segredos), P2, P3…, cada uma ligada aos IDs dos achados, com esforço estimado (baixo/médio/alto).
- i) **Observações fora do escopo.**
- j) **ISSUES PARA O GITHUB** (última seção): para cada achado acionável, o texto completo de uma issue em Markdown dentro de um bloco delimitado por `--- ISSUE n ---` e `--- FIM ISSUE n ---`. Cada issue contém:
  - Título: `[Segurança] <descrição curta da falha>`
  - Labels sugeridas: `security`, `severity:<nível>`, `area:<categoria>`
  - Descrição do problema e por que é explorável
  - Evidência: `arquivo:linha` com trecho de código (segredos sempre mascarados)
  - Impacto
  - Sugestão de correção
  - Critérios de aceite (checklist verificável, incluindo teste automatizado que impeça regressão quando aplicável)
  - Referência ao ID do achado (`SEC-00x`)

Agrupe achados triviais relacionados numa issue única (ex: vários defaults de segredo no mesmo tema). Achados informativos não viram issue.

### 4.3 Issues também como arquivos

`<PASTA_SAIDA>/issues/NN-<slug>.md`, uma por issue, com o mesmo conteúdo do PDF, para facilitar uso com `gh issue create --body-file`. Não crie issues no GitHub — apenas prepare os arquivos.

### 4.4 Script gerador

`<PASTA_SAIDA>/gerar_relatorio.py` (ou equivalente na stack), que lê `findings.json` e gera o PDF e os arquivos de issue, com um `requirements.txt` ou instrução de uso no topo do script.

## 5. GERAÇÃO DO PDF — REGRAS TÉCNICAS

- Ambiente isolado: venv Python com reportlab + matplotlib (ou HTML→PDF se houver navegador headless, wkhtmltopdf ou weasyprint disponível no venv). Crie o venv com `python -m venv <dir>` e use o executável do venv (`<dir>/bin/python` no macOS/Linux, `<dir>\Scripts\python.exe` no Windows).
- A4, margens ~2 cm, cabeçalho com o nome do relatório e rodapé com "Página X de Y" e data.
- Fonte com suporte completo a acentos (ex: DejaVu Sans / DejaVu Sans Mono registradas no reportlab). Não use as fontes base14, que quebram caracteres pt-BR e símbolos como ✔/✘.
- Trechos de código com quebra de linha automática (sem texto saindo da página), escape de `<`, `>` e `&`.
- Tabelas com cabeçalho repetido ao quebrar página, larguras de coluna definidas e texto quebrado dentro das células.
- Evite títulos órfãos no fim da página (`keepWithNext`).
- Gráficos em PNG com DPI ≥ 200 ou em vetor.

### Verificação obrigatória antes de entregar

1. Conte as páginas e confira se o sumário bate com a numeração real.
2. Extraia o texto (pdftotext ou pypdf) e confirme que acentos e símbolos aparecem corretamente.
3. Rasterize todas as páginas (pdftoppm ou pdf2image) e inspecione visualmente: gráficos renderizados, tabelas legíveis, nada cortado ou sobreposto, chips coloridos visíveis.
4. Busque no PDF e nos arquivos de issue por padrões de segredo para garantir que nenhum foi impresso sem máscara.
5. Corrija qualquer defeito e repita a verificação.

## 6. ENTREGA FINAL NO CHAT

- Resumo da stack detectada e do mecanismo de isolamento identificado.
- Placar: total por severidade e por categoria.
- Lista de achados arquivo por arquivo, linha por linha, ordenada por severidade dentro de cada arquivo, com ID, severidade, confiança e uma linha de descrição.
- Pontos fortes verificados (resumido).
- Lacunas de cobertura e limitações (o que não pôde ser verificado estaticamente e por quê).
- Ações imediatas: segredos que devem ser rotacionados agora.
- Caminho de todos os arquivos gerados.

No modo funcionalidade, essa entrega é devolvida à skill chamadora, que a inclui no seu resumo final ao usuário.
