# Matriz Técnica de Auditoria por Stack Tecnológica

Este guia orienta o auditor a mapear e inspecionar com precisão as cinco categorias de segurança nas principais stacks corporativas e modernas.

---

## 1. Banco Sem Tranca (Isolamento de Tenant / Dono / RLS)

### O que procurar:
- **Java (Quarkus / Spring Boot)**:
  - DAOs ou Repositórios executando queries `SELECT` sem condicionar a entidade à conta/tenant do usuário logado.
  - Ausência de filtros automáticos do Hibernate (`@FilterDef`, `@Filter`).
  - Utilização incorreta de instâncias globais ou caches compartilhados entre requisições sem chave de tenant.
- **Node.js / TypeScript (NestJS, Express, Prisma, TypeORM)**:
  - Chamadas `prisma.order.findMany()` ou `repository.find()` sem o predicado `where: { tenantId: user.tenantId }`.
  - Ausência de middleware global ou interceptor que injete o tenant nas transações.
- **Python (FastAPI, Django)**:
  - Managers de modelos customizados que não forçam o filtro pelo `request.user` ou organização.
- **Supabase / PostgreSQL RLS**:
  - Tabelas sem `ALTER TABLE <nome> ENABLE ROW LEVEL SECURITY;`.
  - Políticas com `USING (true)` ou sem validação de `auth.uid() = user_id`.

---

## 2. Permissão Definida no Navegador (Client-Side Only Authorization)

### O que procurar:
- **Frontend**:
  - `v-if="user.role === 'ADMIN'"` ou `{user.isAdmin && <AdminPanel />}` ou diretivas Angular `*hasRole="'ADMIN'"`.
- **Backend correspondente**:
  - Verificar se a rota chamada pelo painel ou ação possui o validador equivalente no servidor:
    - **Quarkus**: `@RolesAllowed("ADMIN")` ou `@Authenticated` (atenção: `@Authenticated` só verifica se está logado, NÃO valida papel!).
    - **Spring Boot**: `@PreAuthorize("hasRole('ADMIN')")`.
    - **Node / NestJS**: `@UseGuards(RolesGuard)` com `@Roles('admin')`.
    - **Express**: Middleware `requireRole('admin')`.

---

## 3. IDOR (Insecure Direct Object Reference)

### O que procurar:
- Parâmetros em rotas REST que indicam chave direta: `/api/pedidos/{id}`, `/api/contas/{numeroConta}`, `/api/arquivos/{uuid}`.
- **Padrão Vulnerável**:
  ```java
  // Inseguro: recupera qualquer pedido pelo ID recebido no path
  Pedido pedido = pedidoDao.findById(id);
  return Response.ok(pedido).build();
  ```
- **Padrão Seguro**:
  ```java
  // Seguro: recupera o pedido apenas se pertencer ao cliente autenticado
  Pedido pedido = pedidoDao.findByIdAndCliente(id, securityContext.getClienteId());
  if (pedido == null) {
      return Response.status(Response.Status.NOT_FOUND).build();
  }
  return Response.ok(pedido).build();
  ```

---

## 4. Chaves Expostas e Defaults Inseguros

### O que procurar:
- **Hardcode em arquivos de configuração**:
  - `application.properties` / `application.yml`:
    - `${DB_PASSWORD:senha123}` ou `${JWT_SECRET:segredo_fraco}`.
    - Se a variável não for informada no ambiente produtivo, o sistema assume o fallback inseguro.
- **Falta de validação no startup**:
  - Se um segredo crítico contiver um valor padrão conhecido ou vazio, a aplicação deve falhar imediatamente na inicialização (`fail-fast`).
- **Arquivos commitados**:
  - `.env`, `.env.production`, arquivos `.pem`, `.key`, `.jks` com senhas padronizadas.

---

## 5. Inputs Sem Tratamento (XSS e Injeções)

### O que procurar:
- **Queries SQL / JPQL Concatenação**:
  - `entityManager.createNativeQuery("SELECT * FROM TAB WHERE NOME = '" + nome + "'")`.
  - **Correção obrigatória**: Parâmetros nomeados (`:nome`) ou posicionais (`?1`).
- **Frontend (XSS)**:
  - React: `dangerouslySetInnerHTML={{ __html: userContent }}`.
  - Angular: `[innerHTML]="userContent"` com bypass de sanitização (`bypassSecurityTrustHtml`).
  - Vue: `v-html="userContent"`.
  - Vanilla JS: `element.innerHTML = ...`.
- **Templates de E-mail e Relatórios**:
  - Interpolação de nome ou comentários de usuário sem escape em templates HTML/PDF.
