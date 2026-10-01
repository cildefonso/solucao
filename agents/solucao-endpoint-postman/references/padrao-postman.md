# Padrão e Estrutura da Coleção Postman para Microsserviços Quarkus

Este documento define os padrões e boas práticas para a geração e manutenção das coleções Postman nos microsserviços Java com Quarkus.

---

## 1. Convenção do Nome e Localização do Arquivo

O arquivo da coleção Postman deve sempre residir na pasta `postman/` na raiz do microsserviço, com o nome derivado diretamente do `<artifactId>` do `pom.xml`:

```xml
<!-- pom.xml -->
<artifactId>siabe-micro</artifactId>
```

Caminho gerado:
```
postman/siabe-micro.postman_collection.json
```

Se o projeto mudar de nome no `pom.xml` (ex: `sicli-micro`), o arquivo correspondente será `postman/sicli-micro.postman_collection.json`.

---

## 2. Resolução da Porta HTTP para a Variável `baseUrl`

A porta do microsserviço deve ser lida a partir de `application-local.properties`:

```properties
# src/main/resources/application-local.properties
quarkus.http.port=8083
```

A variável `baseUrl` da coleção Postman é gerada com essa porta:
```json
{
  "key": "baseUrl",
  "value": "http://localhost:8083",
  "type": "string"
}
```

---

## 3. Mapeamento de Classes Resource para Itens Postman

Cada classe Java anotada com `@Path` mapeia para uma pasta (`folder`) no Postman:

| Anotação Java | Elemento Postman Correspondente |
|---|---|
| `@Tag(name = "...", description = "...")` | `item[].name` e `item[].description` (pasta do recurso) |
| `@Path("/api/recurso")` | Base do caminho da URL |
| `@GET`, `@POST`, `@PUT`, `@DELETE` | `request.method` |
| `@Path("/subpath")` | Elementos de `url.path` |
| `@Operation(summary = "...")` | `item[].name` da requisição |
| `@QueryParam("param")` | Elementos em `url.query` |
| `@PathParam("id")` | `:id` em `url.path` e entrada em `url.variable` |
| `@HeaderParam("X-Header")` | Entradas em `request.header` |
| `@RequestBody` ou Objeto DTO | `request.body.raw` no formato JSON |

---

## 3. Template de Requisição de Exemplo (Schema v2.1.0)

```json
{
  "name": "Consultar Benefício e Conta",
  "request": {
    "method": "GET",
    "header": [
      {
        "key": "Accept",
        "value": "application/json"
      }
    ],
    "url": {
      "raw": "{{baseUrl}}/api/beneficios-contas/v1/consultar?beneficio={{beneficio}}",
      "host": ["{{baseUrl}}"],
      "path": ["api", "beneficios-contas", "v1", "consultar"],
      "query": [
        {
          "key": "beneficio",
          "value": "{{beneficio}}"
        }
      ]
    }
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status code 200', function () {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "const body = pm.response.json();",
          "pm.test('Resposta contém ApiResponse', function () {",
          "    pm.expect(body).to.have.property('resultado');",
          "    pm.expect(body).to.have.property('quantidade');",
          "    pm.expect(body).to.have.property('dados');",
          "});"
        ],
        "type": "text/javascript"
      }
    }
  ]
}
```

---

## 4. Conjunto de Cenários Recomendados por Endpoint

Para cada endpoint REST de negócio, a coleção deve cobrir:

1. **Cenário de Sucesso Padrão (`200 OK` / `201 Created`)**:
   - Com todos os parâmetros essenciais preenchidos.
2. **Cenários de Filtro Alternativo (`200 OK`)**:
   - Quando a consulta aceitar diferentes chaves de busca (ex: consulta por CPF, consulta por Documento/NIT, consulta por Unidade e Conta).
3. **Cenários de Validação de Parâmetros (`400 Bad Request`)**:
   - Requisição sem parâmetros obrigatórios.
   - Parâmetros com formato inválido (ex: CPF com tamanho diferente de 11 dígitos).
   - Valores numéricos fora do intervalo permitido ou negativos.
   - Dígitos verificadores inconsistentes.
4. **Health Check do Recurso (`200 OK`)**:
   - Endpoint `GET /api/<recurso>/health`.
