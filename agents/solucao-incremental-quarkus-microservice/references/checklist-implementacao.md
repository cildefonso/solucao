# Checklist e Padrões de Implementação Incremental

Este documento fornece as diretrizes detalhadas para a adição de novas funcionalidades em projetos estruturados pelo padrão `solucao-quarkus-microservice`.

---

## 1. Mapeamento de Camadas e Responsabilidades

Cada nova funcionalidade deve ser implementada respeitando estritamente a segregação de responsabilidades do padrão:

| Camada | Pacote | Responsabilidade | Padrões Exigidos |
|---|---|---|---|
| **DTO** | `...api.dto` | Contratos de entrada e saída da API | Usar Java Records imutáveis. Anotações de validação (`@NotBlank`, `@NotNull`, `@Min`, `@Max`, `@Pattern`, `@Size`). |
| **Model / Mapper** | `...api.domain.model` | Entidades de banco ou classes de mapeamento | Entidades JPA / PanacheEntityBase ou Mappers estáticos que convertem `Object[]` de queries nativas em DTOs. |
| **DAO** | `...api.domain.dao` | Interação direta com a base de dados | `@ApplicationScoped`. Usar `EntityManager` com parâmetros nomeados (`:param`). Limitar resultados (`setMaxResults`). |
| **Service** | `...api.domain.service` | Regras de negócio e orquestração | `@ApplicationScoped`. `@Transactional` para operações de escrita. Retornar `ApiResponse<T>`. Tratar cenários vazios e exceções de negócio. |
| **Resource** | `...api.resource` | Exposição dos endpoints REST | `@Path`, `@Produces`, `@Consumes`. OpenAPI (`@Operation`, `@APIResponses`, `@Parameter`, `@Tag`). Test Seam para permitir 100% de cobertura. |
| **Exception** | `...api.domain.exception` | Exceções de negócio customizadas | Herdar de `RuntimeException` ou mapear com `ExceptionMapper<E>`. |
| **Utils** | `...api.utils` | Constantes e utilitários | Evitar literais mágicos e duplicações apontadas pelo SonarQube (ex.: limites máximos, queries SQL reutilizáveis). |

---

## 2. Padrão do Endpoint REST (`Resource`) com Test Seam

Para garantir que o código passe pelos testes unitários e de integração com 100% de cobertura (inclusive o bloco `catch` de erro inesperado), utilize o padrão de seam de teste:

```java
package br.com.imac.<projeto>.api.resource;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.eclipse.microprofile.openapi.annotations.Operation;
import org.eclipse.microprofile.openapi.annotations.tags.Tag;
import br.com.imac.<projeto>.api.retorno.ApiResponse;
import br.com.imac.<projeto>.api.domain.service.<Nome>Service;

@Path("/api/<recurso>")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
@Tag(name = "<Nome da Funcionalidade>", description = "<Descrição>")
public class <Nome>Resource {

    private static final Logger LOGGER = LoggerFactory.getLogger(<Nome>Resource.class);
    private static final String CLASSNAME = <Nome>Resource.class.getName();

    @Inject
    <Nome>Service service;

    @GET
    @Path("/health")
    public Response health() {
        String methodName = "health";
        try {
            registrarHealth(methodName);
            return Response.ok("OK").build();
        } catch (Exception e) {
            LOGGER.error(CLASSNAME + " - " + methodName + " - " + e.getMessage(), e);
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).entity(e.getMessage()).build();
        }
    }

    void registrarHealth(String nomeMetodo) {
        LOGGER.info(CLASSNAME + " - " + nomeMetodo);
    }

    @GET
    @Path("/v1/consultar")
    @Operation(summary = "<Resumo>", description = "<Descrição>")
    public Response consultar(@QueryParam("filtro") String filtro) {
        var resposta = service.consultar(filtro);
        return Response.ok(resposta).build();
    }
}
```

---

## 3. Padrão de Serviço (`Service`) com Envelope `ApiResponse<T>`

```java
package br.com.imac.<projeto>.api.domain.service;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.List;
import br.com.imac.<projeto>.api.dto.<Nome>Response;
import br.com.imac.<projeto>.api.retorno.ApiResponse;
import br.com.imac.<projeto>.api.enums.ResultadoConsulta;
import br.com.imac.<projeto>.api.domain.dao.<Nome>Dao;

@ApplicationScoped
public class <Nome>Service {

    private static final Logger LOGGER = LoggerFactory.getLogger(<Nome>Service.class);

    @Inject
    <Nome>Dao dao;

    public ApiResponse<<Nome>Response> consultar(String filtro) {
        List<<Nome>Response> itens = dao.buscarPorFiltro(filtro);

        if (itens.isEmpty()) {
            return ApiResponse.of(ResultadoConsulta.NAO_LOCALIZADO, "Nenhum registro encontrado.", itens);
        }

        return ApiResponse.of(ResultadoConsulta.SUCESSO, "Consulta realizada com sucesso.", itens);
    }
}
```

---

## 4. Estratégia de Testes para Cobertura 100%

Ao adicionar a nova funcionalidade, implementar obrigatoriamente:

1. **Teste do Service (`<Nome>ServiceTest.java`)**:
   - Cenário com retorno preenchido (valida `ResultadoConsulta.SUCESSO` e dados).
   - Cenário com lista vazia (valida `ResultadoConsulta.NAO_LOCALIZADO`).
   - Mock ou stub do DAO com Mockito ou subclasse local.

2. **Teste do Resource (`<Nome>ResourceTest.java`)**:
   - Teste de chamada com sucesso (`200 OK`).
   - Teste do endpoint `/health` retornando `200 OK`.
   - Teste do endpoint `/health` forçando exceção via subclasse que sobrescreve `registrarHealth(...)` para garantir cobertura do bloco `catch` (`500 Internal Server Error`).
   - Teste de validação de parâmetros com valores inválidos se houver Bean Validation (HTTP `400 Bad Request`).

3. **Teste do Mapper / DTO (`<Nome>MapperTest.java`)**:
   - Teste de mapeamento com valores válidos, nulos ou casos de borda.

---

## 5. Atualização da Coleção Postman

Sempre que um novo endpoint for criado ou modificado, adicionar a requisição correspondente em `postman/<PROJETO>.postman_collection.json`:
- Definir método HTTP correto (`GET`, `POST`, `PUT`, `DELETE`).
- URL apontando para `{{baseUrl}}/api/<recurso>/...`.
- Headers: `Accept: application/json` e `Content-Type: application/json`.
- Query params ou body de exemplo.
