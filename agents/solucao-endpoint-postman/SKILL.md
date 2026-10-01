---
name: solucao-endpoint-postman
description: 'Lê as classes Java que contêm os endpoints (Resource JAX-RS / Quarkus REST) do microsserviço e gera ou atualiza a coleção Postman correspondente. Obtém o nome do arquivo da coleção dinamicamente a partir da tag <artifactId> do pom.xml (ex: <artifactId>.postman_collection.json dentro da pasta postman/). Mapeia rotas, query params, path params, corpos de requisição DTO, scripts de teste de validação e de contrato.'
argument-hint: 'Nome do arquivo ou escopo de endpoints a mapear (ex: atualizar todos os endpoints ou recurso específico)'
user-invocable: true
---

# Extração de Endpoints e Geração da Coleção Postman

Esta skill automatiza a inspeção das classes Java de controle/exposição REST (`Resource`) no projeto Quarkus e gera ou atualiza a coleção de testes do **Postman** (schema v2.1.0).

O nome do arquivo da coleção gerada é obtido dinamicamente a partir do `pom.xml` do projeto:
```
postman/<artifactId>.postman_collection.json
```
*(Por exemplo, em um projeto com `<artifactId>siabe-micro</artifactId>`, o arquivo gerado será `postman/siabe-micro.postman_collection.json`).*

---

## Quando Utilizar Esta Skill

- Quando o usuário solicitar:
  - *"Gerar coleção Postman do projeto"*
  - *"Atualizar Postman com os endpoints das classes Resource"*
  - *"Criar Postman baseado nos endpoints existentes"*
  - *"Incluir novos endpoints no Postman a partir do código Java"*
  - *"Mapear rotas e testes automáticos no Postman para o microsserviço"*

---

## 1. Fase 1: Identificação do Nome do Arquivo e Configurações

Antes de inspecionar os endpoints, o agente **DEVE LER** as configurações fundamentais do projeto:

1. **Leitura do `pom.xml`**:
   - Localizar a tag `<artifactId>` (ex.: `<artifactId>siabe-micro</artifactId>`).
   - Definir o caminho de saída da coleção Postman:
     ```
     postman/${artifactId}.postman_collection.json
     ```
   - Garantir que a pasta `postman/` exista no projeto.

2. **Leitura Obrigatória da Porta HTTP em `application-local.properties`**:
   - Localizar e inspecionar o arquivo `application-local.properties` (procurando em `src/main/resources/application-local.properties` ou na raiz do projeto).
   - Extrair o valor da porta configurada em `quarkus.http.port` (exemplo: `quarkus.http.port=8083`).
   - Caso `application-local.properties` não exista ou não contenha a chave `quarkus.http.port`, verificar como fallback em `src/main/resources/application.properties` ou utilizar `8080` como padrão.
   - Definir o valor da variável de coleção `baseUrl` no Postman utilizando a porta extraída:
     ```json
     {
       "key": "baseUrl",
       "value": "http://localhost:<porta_local>",
       "type": "string"
     }
     ```
     *(Exemplo: se `quarkus.http.port=8083` em `application-local.properties`, `baseUrl` será `http://localhost:8083`)*.

3. **Leitura das Configurações Gerais (`application.properties` / `application-local.properties`)**:
   - Identificar o path base da API caso haja `quarkus.http.root-path` ou prefixos globais.
   - Identificar políticas de segurança (`quarkus.http.auth.*`, OIDC) para determinar cabeçalhos ou permissões de health.

---

## 2. Fase 2: Varredura das Classes de Endpoints (`Resource`)

O agente deve localizar e inspecionar todos os arquivos Java que definem endpoints REST:

1. **Localização**:
   - Buscar em `src/main/java/**/resource/*Resource.java` ou qualquer classe anotada com `@Path`.

2. **Extração de Metadados da Classe**:
   - Anotação `@Path("...")`: prefixo do recurso (ex.: `@Path("/api/beneficios-contas")`).
   - Anotação `@Tag(name = "...", description = "...")`: utilizada para definir o nome e descrição da pasta/grupo de requisições no Postman.
   - Anotação `@Produces(...)` e `@Consumes(...)`: valores padrão de headers (`Accept`, `Content-Type`).

3. **Extração de Cada Método de Endpoint**:
   - **Método HTTP**: `@GET`, `@POST`, `@PUT`, `@DELETE`, `@PATCH`, etc.
   - **Subpath do método**: `@Path("...")` (ex.: `@Path("/v1/consultar")`, `@Path("/health")`).
   - **OpenAPI**:
     - `@Operation(summary = "...", description = "...")` para definir o `name` e `description` do item de requisição.
     - `@APIResponse(responseCode = "...", description = "...")` para entender os códigos de status esperados.
   - **Parâmetros**:
     - `@QueryParam("nome")`: adicionado à lista `query` da URL.
     - `@PathParam("nome")`: adicionado ao array `path` e à lista `variable` da URL.
     - `@HeaderParam("nome")`: adicionado ao array `header`.
     - **Corpo da Requisição (Body)**: se houver parâmetro DTO (Java Record ou classe) em métodos POST/PUT, inspecione a definição do DTO em `dto/` para construir um exemplo JSON válido (`raw`) preenchendo os tipos de dados e respeitando validações (`@NotNull`, `@NotBlank`, `@Min`, `@Pattern`).

---

## 3. Fase 3: Estruturação da Coleção Postman (Schema v2.1.0)

A coleção deve seguir rigorosamente a especificação do Postman Schema v2.1.0:

### 3.1. Seção `info`
```json
{
  "_postman_id": "<uuid-ou-hash>",
  "name": "<Nome do Projeto ou Sigla>",
  "description": "Coleção de testes e documentação dos endpoints da API <artifactId>.",
  "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
}
```

### 3.2. Seção `variable`
Definir variáveis de ambiente da coleção para facilitar a execução em diferentes ambientes:
- `baseUrl`: `http://localhost:<porta>` com a porta extraída de `application-local.properties` (ex.: `http://localhost:8083`).
- Variáveis para cada parâmetro relevante identificado nos endpoints (ex.: `beneficio`, `cpf`, `nit`, `unidadePv`, `conta`, `dataReferencia`, `dataCorte`, etc.).

### 3.3. Organização em Pastas (`item`)
Criar uma pasta por grupo funcional:
1. **Pasta Health**:
   - `Health check global`: `GET {{baseUrl}}/q/health`
   - `Health liveness`: `GET {{baseUrl}}/q/health/live`
   - `Health readiness`: `GET {{baseUrl}}/q/health/ready`
2. **Pastas de Recursos de Negócio** (uma para cada `@Tag` / Resource):
   - **Health do Recurso**: `GET {{baseUrl}}/api/<recurso>/health`.
   - **Requisições de Sucesso (`200 OK` / `201 Created`)**:
     - Chamada com parâmetros principais e com filtros alternativos.
     - Exemplo: `Consultar por NB`, `Consultar por CPF`, `Consultar por NIT`, `Consultar por Conta`.
     - Chamada completa com todos os parâmetros preenchidos.
   - **Requisições de Validação de Negócio (`400 Bad Request`)**:
     - Consulta sem parâmetros obrigatórios.
     - Consulta com campos inválidos (ex.: CPF malformatado, benefício zerado/negativo, DV inválido).

### 3.4. Scripts de Teste Automático (`event` do Postman)
Para cada requisição, incluir script de validação em JavaScript:
- Validação de código de status HTTP:
  ```javascript
  pm.test('Status code 200', function () {
      pm.response.to.have.status(200);
  });
  ```
- Validação de formato da resposta:
  ```javascript
  const body = pm.response.json();
  pm.test('Resposta possui contrato ApiResponse', function () {
      pm.expect(body).to.have.property('resultado');
      pm.expect(body).to.have.property('quantidade');
      pm.expect(body).to.have.property('dados');
  });
  ```
- Validação de cenários de erro (`400 Bad Request`):
  ```javascript
  pm.test('Retorna erro 400 para parâmetro inválido', function () {
      pm.response.to.have.status(400);
  });
  ```

---

## 4. Fase 4: Preservação e Mesclagem com Coleções Existentes

- Se o arquivo `postman/${artifactId}.postman_collection.json` já existir:
  - O agente deve **ler o arquivo existente** para preservar variáveis personalizadas, tokens de autenticação ou scripts customizados previamente adicionados pelo usuário.
  - Atualizar ou adicionar novas pastas e itens de requisição sem corromper a estrutura prévia.
- Se existir uma coleção antiga com nome diferente (ex.: `postman/NOME-LEGADO.postman_collection.json`):
  - Manter compatibilidade ou sincronizar os endpoints mantendo o padrão canônico `${artifactId}.postman_collection.json`.

---

## 5. Fase 5: Validação do Arquivo Gerado e Ciclo de Execução

1. **Validação Sintática**:
   - Verificar se o JSON gerado é estritamente válido:
     ```powershell
     Get-Content postman\<artifactId>.postman_collection.json | ConvertFrom-Json | Out-Null
     ```

2. **Validação com a Aplicação Local**:
   - Validar se os endpoints descritos na coleção correspondem aos caminhos registrados na aplicação.
   - Testar o health check via PowerShell:
     ```powershell
     Invoke-RestMethod -Uri "http://localhost:<porta>/api/<recurso>/health" -Method Get
     ```

---

## Recursos e Referências

- [Padrão e Estrutura da Coleção Postman](./references/padrao-postman.md)
