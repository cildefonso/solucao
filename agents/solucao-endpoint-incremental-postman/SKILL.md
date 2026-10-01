---
name: solucao-endpoint-incremental-postman
description: 'Adiciona incrementalmente endpoints de novas classes Java (Resource JAX-RS / Quarkus REST) a uma coleção Postman pré-existente (obtida a partir do <artifactId> do pom.xml ou coleção indicada). Requer que o arquivo JSON da coleção Postman já exista previamente (gerado pela skill solucao-endpoint-postman). Lê a porta HTTP em application-local.properties, inspeciona as novas classes Resource, mescla as novas pastas, requisições (200, 400, health) e variáveis sem sobrescrever ou perder itens já existentes.'
argument-hint: 'Nome ou caminho da nova classe Resource (ex: NovoResource.java ou br.com.imac.<projeto>.api.resource.NovoResource)'
user-invocable: true
---

# Adição Incremental de Endpoints na Coleção Postman

Esta skill guia e executa a **inclusão incremental** de endpoints de novas classes Java de controle REST (`Resource`) em uma coleção de testes do **Postman** (schema v2.1.0) que já existe no projeto.

Ela complementa e utiliza como referência a skill **`solucao-endpoint-postman`**, operando sob o princípio de **modificação não-destrutiva**: preserva todas as variáveis, pastas, requisições e scripts pré-existentes na coleção.

---

## Pré-requisito Obrigatório: Existência do Arquivo Postman

> **REGRA FUNDAMENTAL**: O arquivo JSON da coleção Postman **DEVE EXISTIR** antes da execução desta skill.

1. O agente identifica o caminho padrão da coleção a partir do `<artifactId>` no `pom.xml`:
   ```
   postman/<artifactId>.postman_collection.json
   ```
2. O agente verifica se o arquivo existe na pasta `postman/`:
   - **Se o arquivo existir**: procede imediatamente com a leitura e o incremento não-destrutivo.
   - **Se o arquivo NÃO existir**:
     - O agente deve interromper o fluxo incremental e informar ao usuário que a coleção base não foi encontrada.
     - Deve sugerir ou acionar a skill **`solucao-endpoint-postman`** para gerar a coleção inicial completa antes de realizar adições incrementais.

---

## Quando Utilizar Esta Skill

- Quando uma nova classe `Resource` for criada no projeto (ex.: após o fluxo da skill `solucao-incremental-quarkus-microservice`).
- Quando o usuário solicitar:
  - *"Adicionar endpoints da nova classe no Postman existente"*
  - *"Incrementar o postman com a classe <Nome>Resource"*
  - *"Incluir novo endpoint sem sobrescrever a coleção atual"*
  - *"Atualizar a coleção postman com a funcionalidade recém-criada"*

---

## 1. Fase 1: Validação do Arquivo e Resolução de Configurações

1. **Localizar e Validar o Arquivo Postman Existente**:
   - Ler `<artifactId>` no `pom.xml` (ex: `siabe-micro` -> `postman/siabe-micro.postman_collection.json`).
   - Carregar e validar o JSON existente:
     ```powershell
     $colecao = Get-Content postman\<artifactId>.postman_collection.json -Raw -Encoding UTF8 | ConvertFrom-Json
     ```

2. **Leitura da Porta HTTP em `application-local.properties`**:
   - Inspecionar `src/main/resources/application-local.properties` (ou raiz).
   - Extrair o valor de `quarkus.http.port` (ex: `8083`).
   - Verificar se a variável `baseUrl` da coleção existente está sincronizada com essa porta (ex: `http://localhost:8083`), atualizando-a se necessário.

---

## 2. Fase 2: Identificação da Nova Classe Resource

1. **Determinar a Nova Classe**:
   - Obter a classe pelo parâmetro do usuário (ex.: `BeneficioContaResource.java`, `ContratoResource.java`).
   - Ou identificar via `git status` / busca por novas classes em `src/main/java/**/resource/*Resource.java` que ainda não constam na coleção Postman.

2. **Extrair Metadados do Novo Resource**:
   - Anotação `@Path("...")`: prefixo base das rotas (ex.: `@Path("/api/contratos")`).
   - Anotação `@Tag(name = "...", description = "...")`: define o nome da pasta no Postman correspondente à nova funcionalidade.
   - Anotação `@Produces(...)` e `@Consumes(...)`: cabeçalhos padrão (`Accept`, `Content-Type`).

3. **Mapear Métodos e Parâmetros da Nova Classe**:
   - **Health local do recurso**: `GET {{baseUrl}}/api/<recurso>/health` (se implementado com o padrão de test seam).
   - **Operações REST** (`@GET`, `@POST`, `@PUT`, `@DELETE`):
     - Caminho relativo do método (`@Path`).
     - Resumo e descrição (`@Operation`).
     - Parâmetros de consulta (`@QueryParam`).
     - Parâmetros de caminho (`@PathParam`).
     - Cabeçalhos (`@HeaderParam`).
     - Corpo da requisição (DTOs para POST/PUT). Quando houver DTO, inspecionar a classe/record em `dto/` para construir payload de exemplo válido com campos obrigatórios (`@NotNull`, `@NotBlank`).

---

## 3. Fase 3: Estruturação dos Novos Itens da Pasta

Para a nova funcionalidade, montar o grupo de requisições no formato Postman Schema v2.1.0:

1. **Health Check do Recurso**:
   - Endpoint: `GET {{baseUrl}}/api/<recurso>/health`
   - Teste: validação de retorno `200 OK`.

2. **Cenários de Sucesso (`200 OK` / `201 Created`)**:
   - Cenário padrão com todos os campos preenchidos.
   - Cenários alternativos para filtros opcionais ou critérios de busca múltiplos.
   - Script de teste:
     ```javascript
     pm.test('Status code 200', function () {
         pm.response.to.have.status(200);
     });
     const body = pm.response.json();
     pm.test('Resposta possui contrato ApiResponse', function () {
         pm.expect(body).to.have.property('resultado');
         pm.expect(body).to.have.property('quantidade');
         pm.expect(body).to.have.property('dados');
     });
     ```

3. **Cenários de Validação e Regras de Negócio (`400 Bad Request`)**:
   - Chamada sem os parâmetros obrigatórios.
   - Chamada com parâmetros em formatos inválidos (ex: documento com tamanho errado, valor zero/negativo, etc.).
   - Script de teste:
     ```javascript
     pm.test('Retorna erro 400 para parâmetro inválido', function () {
         pm.response.to.have.status(400);
     });
     ```

---

## 4. Fase 4: Mesclagem Incremental Não-Destrutiva

Ao atualizar o arquivo JSON existente:

1. **Atualização da Seção `variable`**:
   - Adicionar novas variáveis de coleção apenas se ainda não existirem (ex: novos IDs, códigos de documento, datas).
   - Nunca sobrescrever ou remover variáveis existentes de outras funcionalidades.

2. **Atualização da Seção `item` (Pastas)**:
   - Verificar se já existe uma pasta com o nome da tag (`@Tag.name`):
     - **Caso NÃO exista**: criar nova pasta `{ "name": "<Tag>", "item": [ ...novos itens... ] }` e anexar à lista `item`.
     - **Caso já exista**: mesclar os itens, adicionando apenas requisições novas e mantendo as existentes intactas.

3. **Gravação Segura**:
   - Salvar o arquivo no caminho `postman/<artifactId>.postman_collection.json`.
   - Utilizar codificação UTF-8 sem BOM para preservar caracteres acentuados.

---

## 5. Fase 5: Validação e Ciclo de Execução

Seguindo o ciclo de vida do projeto:

1. **Validação do JSON**:
   ```powershell
   Get-Content postman\<artifactId>.postman_collection.json | ConvertFrom-Json | Out-Null
   ```

2. **Validação com a Aplicação**:
   - Confirmar se o endpoint novo responde na porta configurada:
     ```powershell
     Invoke-RestMethod -Uri "http://localhost:<porta>/api/<novo-recurso>/health" -Method Get
     ```

---

## Recursos e Referências

- [Guia de Incremento Não-Destrutivo do Postman](./references/guia-incremento-postman.md)
- [Padrão Base da Coleção Postman](../solucao-endpoint-postman/references/padrao-postman.md)
