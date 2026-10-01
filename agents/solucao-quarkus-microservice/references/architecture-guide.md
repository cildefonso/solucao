# Guia de Arquitetura em Camadas (Padrão SIABE-micro)

Este guia documenta o padrão arquitetural em camadas adotado no `SIABE-micro`, otimizado para microsserviços Quarkus de alta performance, fácil manutenção e conformidade com SonarQube e cobertura de testes de 100%.

---

## 1. Organização dos Pacotes

O pacote base segue a convenção: `<prefixo-do-pacote>.<sistema>.api` (padrão sugerido: `br.com.imac.<sistema>.api`)

```
<prefixo-do-pacote>.<sistema>.api/
├── domain/
│   ├── dao/                 # Acesso a dados (EntityManager, Panache, Native Queries)
│   ├── exception/           # ExceptionMappers JAX-RS customizados
│   ├── model/               # Entidades JPA, registros de banco e Mappers de domínio
│   └── service/             # Regras de negócio, transações (@Transactional) e orquestração
├── dto/                     # Records Java imutáveis para transferência de dados (Request/Response)
├── enums/                   # Enums de domínio e status de operação (ex: ResultadoConsulta)
├── resource/                # Endpoints JAX-RS / Quarkus REST com OpenAPI e validações
├── retorno/                 # Envelope padrão de resposta de API (ApiResponse<T>)
└── utils/                   # Utilitários, constantes e limites de consulta
```

---

## 2. Padrões por Camada

### 2.1. Envelope de Retorno (`ApiResponse<T>`)
Toda resposta da API deve seguir um envelope único padronizado:

```java
package br.com.imac.<sistema>.api.retorno;

import br.com.imac.<sistema>.api.enums.ResultadoConsulta;
import java.time.OffsetDateTime;
import java.util.List;

public record ApiResponse<T>(
        ResultadoConsulta resultado,
        String mensagem,
        int quantidade,
        OffsetDateTime dataHora,
        List<T> dados) {

    public static <T> ApiResponse<T> of(ResultadoConsulta resultado, String mensagem, List<T> dados) {
        return new ApiResponse<>(resultado, mensagem, dados.size(), OffsetDateTime.now(), dados);
    }
}
```

### 2.2. Camada Resource (`@Path`)
- Expõe endpoints REST com boas práticas de documentação OpenAPI/Swagger.
- Deve conter endpoint de `/health` próprio ou expor health check SmallRye.
- **Padrão de Testabilidade (Test Seam)**: Para métodos com tratamento de exceções internas em blocos `try-catch`, fornecer um método package-private auxiliar (ex: `registrarHealth()`) permitindo que testes unitários simulem falhas sem necessidade de reflection ou instrumentação de bytecode:

```java
@GET
@Path("/health")
public Response health() {
    try {
        registrarHealth("OK");
        return Response.ok(ApiResponse.of(ResultadoConsulta.SUCESSO, "Serviço operacional", List.of())).build();
    } catch (Exception e) {
        return Response.serverError().entity(ApiResponse.of(ResultadoConsulta.ERRO_INTERNO, e.getMessage(), List.of())).build();
    }
}

void registrarHealth(String status) {
    // Implementação padrão
}
```

### 2.3. Camada Service (`@ApplicationScoped`)
- Contém regras de negócio e validações.
- Utiliza `@Transactional` (quando necessário escrita/leitura atômica).
- Delega queries complexas ou native queries para a camada DAO.
- Retorna `ApiResponse<T>` ou objetos de domínio já mapeados para DTOs.

### 2.4. Camada DAO / Persistência
- Pode utilizar Hibernate com Panache (`PanacheRepositoryBase`) ou injeção de `EntityManager`.
- Native Queries para bancos corporativos legados (ex: IBM DB2 Mainframe ou Linux/Windows).
- Conversão segura de colunas e tipos de dados.

### 2.5. Camada Exception (`ExceptionMapper<T>`)
- Mapeamento explícito de exceções de banco (ex: `DB2Exception` / `PersistenceException`) e validação.
- Respostas consistentes no envelope `ApiResponse<Void>` ou formato JSON estruturado com status HTTP adequado (400, 404, 500).

---

## 3. Padrões de Qualidade SonarQube

Para evitar apontamentos comuns no Sonar:
1. **Sem literais de String duplicados**:
   - Reutilizar constantes `public static final String` em classes utilitárias ou locais nos testes (ex: `SQL_TESTE`, `CHAVE_MENSAGEM`, `CHAVE_TIMESTAMP`).
2. **Métodos de teste claros e independentes**:
   - Nomes descritivos (ex: `deveRetornarSucessoQuandoParametrosValidos`).
   - Asserções explícitas com `assertEquals`, `assertNotNull`, `assertTrue`.
3. **Visibilidade adequada**:
   - Injeções em testes com visibilidade de pacote quando necessário para stubs limpos.
