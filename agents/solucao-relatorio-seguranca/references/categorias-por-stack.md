# Categorias por stack — playbook de varredura

Carregue na FASE 1 (mapeamento) e na FASE 3 (varredura) de `/hm-security-report`.

Cada categoria tem: **o que é**, **o equivalente por stack**, **onde procurar**, **o que confirma o achado** e **o que é falso positivo**. Os comandos usam `rg` (ripgrep); adapte se não houver.

Regra que vale para as cinco: **grep produz candidatos; só a leitura do arquivo produz achado.**

---

## 1. Banco sem tranca — isolamento de inquilino/dono

**O que é.** Consulta que devolve linhas sem restringir ao usuário autenticado ou à organização/workspace/tenant dele. O vetor não é uma rota específica: é a consulta.

**Primeiro, determine o mecanismo do projeto.** A resposta muda tudo:

| Mecanismo | Como se parece | Onde a falha mora |
|---|---|---|
| RLS (Supabase/Postgres) | `CREATE POLICY`, `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` | Tabela sem RLS habilitado; política `USING (true)`; uso da `service_role` key no servidor, que **ignora RLS** |
| Filtro global do ORM | `@Filter` do Hibernate, `prisma.$extends`, escopo default do Django/Rails | Query que escapa do escopo (`unscoped`, `raw`, `objects.all()`), ou filtro não ativado na sessão |
| Middleware de tenant | `req.tenantId` populado e usado no repositório | Handler que usa o cliente de banco direto, sem passar pelo repositório |
| Filtro manual | predicado escrito à mão em cada query | Qualquer query onde alguém esqueceu — o modo mais comum de falhar |
| **Nenhum** | — | O projeto inteiro. Este é o achado central, não um item de lista |

**Onde procurar:**

```bash
rg -n "findAll|listAll|\.all\(\)|objects\.all|SELECT \*|aggregate|groupBy|createQueryBuilder|export|report" --glob '!**/test/**'
```

```bash
rg -n "ENABLE ROW LEVEL SECURITY|CREATE POLICY" -g '*.sql'
```

```bash
rg -n "SERVICE_ROLE|service_role|SUPABASE_SERVICE"
```

**Confirma o achado:** a consulta é alcançável por um handler autenticado **e** o predicado de tenant/dono não existe nem na consulta, nem no repositório, nem numa política de banco, nem num filtro global ativo.

**Falso positivo:** consulta em job/CLI/migration sem rota; tabela genuinamente pública (catálogo, países, planos); consulta já restrita por join com tabela que o filtro cobre; endpoint de admin de plataforma com papel validado no servidor.

**Ponto que quase todo mundo perde:** relatórios, exportações, contadores e agregações. Costumam ser escritos fora do repositório padrão e são o caminho mais fácil de vazar tudo de uma vez.

---

## 2. Permissão definida no navegador

**O que é.** O frontend esconde a UI por papel; o servidor não repete a checagem. A UI vira sugestão.

**Equivalentes por stack (lado servidor):** `@RolesAllowed`/`@PreAuthorize` (Java), `permission_classes`/`@permission_required` (Django/DRF), `Depends(require_role)` (FastAPI), CanCan/Pundit (Rails), Guards (NestJS), middleware `requireRole` (Express), Gate/Policy (Laravel), checagem manual dentro do handler.

**Método — cruzamento, não busca solta:**

1. Liste todo gate de papel no frontend:

```bash
rg -n "isAdmin|isOwner|canEdit|hasRole|hasPermission|role ===|permissions\.|RoleGuard" --glob '**/{src,app,web,frontend}/**'
```

2. Para **cada** gate, descubra qual endpoint o elemento protegido aciona.
3. Abra o handler desse endpoint e verifique se existe checagem de papel **no servidor**.
4. Faça o caminho inverso: liste as rotas administrativas do backend e cheque se todas exigem papel.

```bash
rg -n "/admin|/manage|/settings|/users|/billing|/roles|/impersonate"
```

**Confirma o achado:** o endpoint executa a operação privilegiada exigindo apenas autenticação — ou nada.

**Falso positivo:** a checagem existe numa camada acima (guard global, middleware de router, decorator na classe em vez do método) — verifique a classe e o router inteiros antes de acusar; a operação não é privilegiada de fato (o usuário edita o próprio recurso); a UI esconde por conveniência, não por permissão.

**Severidade:** promoção/rebaixamento de papel, impersonação, alteração de billing e gestão de usuários são **Alta** ou **Crítica**. Esconder um botão de exportar é **Média**.

---

## 3. IDOR — objeto por ID sem verificação de posse

**O que é.** O handler recebe um identificador do cliente (path, query, body, header) e busca/atualiza/apaga o objeto sem checar a quem ele pertence.

**Método: percorra TODOS os handlers.** Esta categoria não admite amostragem. Monte a lista completa primeiro:

```bash
rg -n "@(Get|Post|Put|Patch|Delete)Mapping|@(GET|POST|PUT|DELETE)|app\.(get|post|put|patch|delete)|router\.(get|post|put|patch|delete)|@app\.(get|post)|@router\.(get|post)"
```

Depois, para cada handler que recebe identificador:

```bash
rg -n "findById|findByPk|get_object_or_404|findUnique|findOne\(|params\.id|PathParam|PathVariable|pk=|where: \{ id"
```

**Confirma o achado:** existe caminho da entrada até o acesso ao dado sem comparação com a identidade do chamador — nem na consulta, nem depois dela, nem em política de banco.

**Falso positivo:** identificador opaco e não enumerável **e** recurso público por design (link compartilhável); objeto global (plano, país); posse validada logo abaixo, num service; policy/RLS cobrindo.

**Detalhe que separa auditor bom de ruim:** verifique o **update parcial**. `PATCH /pedidos/{id}` com body `{ "clienteId": 999 }` pode reatribuir o objeto a outro dono mesmo com a posse validada na leitura. Campo de posse nunca vem do cliente.

**Padrão correto a reconhecer (vira ponto forte):** a posse entra **na própria consulta** (`where id = ? AND org_id = ?`) e a resposta para acesso cruzado é **404**, não 403 — 403 confirma que o recurso existe.

---

## 4. Chaves expostas — segredos hardcoded

**O que é.** Credencial que existe no repositório: literal no código, default em config, valor em CI, ou apagada no working tree mas viva no histórico.

**Onde procurar — código, config, infra, CI, docs:**

```bash
rg -n "(?i)(api[_-]?key|secret|token|password|credential|private[_-]?key)\s*[:=]\s*['\"][^'\"]{8,}"
```

```bash
rg -n "sk_live_|sk_test_|AKIA[0-9A-Z]{16}|ghp_|xox[baprs]-|AIza[0-9A-Za-z_-]{35}|BEGIN [A-Z ]*PRIVATE KEY"
```

**Defaults que viram segredo real — o caso mais perigoso e o mais ignorado:**

```bash
rg -n '\$\{[A-Z_]+:-[^}]+\}|os\.getenv\([^)]+,\s*"[^"]+|process\.env\.[A-Z_]+\s*\|\|\s*"'
```

Um `${JWT_SECRET:-dev-secret}` não é inofensivo: se a variável não for injetada no ambiente de destino, a aplicação **sobe assinando token com um segredo público** e ninguém percebe. Cheque também a **ausência de validação de startup**: existe código que recusa iniciar sem a variável, ou que rejeita valores de uma lista proibida? Se não existe, isso é parte do achado.

**Histórico git — segredo removido continua acessível:**

```bash
git log --all --oneline -S "PRIVATE KEY" | head -20
```

```bash
git log --all -p -S "sk_live_" | head -60
```

**Bundle do frontend — chave embutida no build é pública:**

```bash
rg -n "VITE_|NEXT_PUBLIC_|REACT_APP_|PUBLIC_" --glob '!node_modules'
```

Prefixo público com nome de segredo (`NEXT_PUBLIC_..._SECRET`, `VITE_SERVICE_KEY`) é achado, não estilo.

**Falso positivo:** chave publicável por design (`pk_live_`, Supabase anon key com RLS ativo, Firebase web config); fixture de teste com valor obviamente falso; placeholder (`<your-key-here>`, `changeme` em `.env.example`).

**Severidade:** segredo de assinatura (JWT, webhook) e chave de provedor com escrita = **Crítica**. Credencial de dev sem alcance externo = **Baixa**, com a ressalva de reuso entre ambientes.

**Sempre:** mascare o valor real no relatório. Recomende **rotação**, não só remoção — o segredo vazou no momento em que foi commitado.

---

## 5. Inputs sem tratamento — XSS e injeção em template

**O que é.** Texto controlado pelo usuário chega a um interpretador de HTML/JS sem escape.

**Frontend — sinks por framework:**

| Framework | Sink |
|---|---|
| React | `dangerouslySetInnerHTML` |
| Vue | `v-html` |
| Angular | `[innerHTML]`, `bypassSecurityTrustHtml` |
| Svelte | `{@html ...}` |
| DOM puro | `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write` |
| Qualquer | `eval`, `new Function`, `setTimeout("string")` |

```bash
rg -n "dangerouslySetInnerHTML|v-html|\[innerHTML\]|bypassSecurityTrust|\{@html|innerHTML\s*=|insertAdjacentHTML|document\.write|eval\(|new Function\("
```

**URLs controladas pelo usuário** em `href`/`src`/`action` — `javascript:` e `data:text/html` executam:

```bash
rg -n "href=\{|src=\{|:href=|\[href\]|window\.open\(|location\.href\s*="
```

**Markdown/HTML renderizado:** `marked`, `markdown-it`, `showdown` só são seguros com sanitização explícita. Procure a lib de sanitização e confirme que ela é **aplicada no ponto encontrado**, não apenas instalada:

```bash
rg -n "dompurify|DOMPurify|sanitize-html|bleach|jsoup|htmlspecialchars|sanitizer" package.json requirements.txt pom.xml composer.json
```

**Backend — o lado que quase ninguém audita:**

- Templates de e-mail com interpolação crua (Qute, Thymeleaf, Jinja com `|safe`, ERB com `raw`/`html_safe`, Blade com `{!! !!}`, Handlebars com `{{{ }}}`).
- Respostas que devolvem HTML montado por concatenação.
- Mensagens de erro que ecoam a entrada dentro de HTML.

```bash
rg -n "\|safe|html_safe|raw\(|\{!!|\{\{\{|Markup\(|mark_safe|@Html\.Raw"
```

**Confirma o achado:** o dado que chega no sink tem origem em entrada de usuário (formulário, API, upload, parâmetro de URL, campo de perfil) e não passa por sanitizador no caminho.

**Falso positivo:** conteúdo constante ou vindo de CMS confiável com fluxo de aprovação; dado já sanitizado a montante (comprove lendo); `dangerouslySetInnerHTML` com string literal do próprio código.

**Distinga no relatório:** XSS **armazenado** (payload persiste e atinge outros usuários) é mais grave que **refletido** (exige que a vítima clique num link preparado). Diga qual dos dois é.

**Se o projeto não tem frontend:** declare a categoria não aplicável ao lado cliente e audite **apenas** o lado servidor (templates, e-mails, respostas HTML). Se não houver nem isso, registre em `categorias_nao_aplicaveis` com o motivo. Não invente achado.
