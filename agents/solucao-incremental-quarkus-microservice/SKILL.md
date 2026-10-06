---
name: solucao-incremental-quarkus-microservice
description: 'Adiciona novas funcionalidades incrementais a um microsserviço Java Quarkus corporativo existente (criado previamente pela skill solucao-quarkus-microservice). Identifica automaticamente a estrutura e pacotes do projeto atual, coleta os requisitos da nova funcionalidade, cria as classes em camadas (DTO, Model, DAO, Service, Resource com test seam), implementa testes unitários/integrados com 100% de cobertura, atualiza a coleção Postman e valida com build e reinicialização local.'
argument-hint: 'Descrição da nova funcionalidade (ex: consulta de benefícios, cadastro de proposta, cancelamento de contrato)'
user-invocable: true
---

# Desenvolvimento Incremental de Novas Funcionalidades em Microsserviços Quarkus

Esta skill guia e executa o desenvolvimento de **novas funcionalidades** de forma incremental em projetos de microsserviços Java com Quarkus criados a partir do padrão arquitetural de referência do **`solucao-quarkus-microservice`**.

---

## Quando Utilizar Esta Skill

- Quando o projeto base já existe (criado ou alinhado com a skill `solucao-quarkus-microservice`).
- Quando o usuário solicitar:
  - *"Criar nova funcionalidade no projeto"*
  - *"Adicionar novo endpoint / recurso REST"*
  - *"Implementar consulta / cadastro / operação de negócio no microsserviço"*
  - *"Criar novo DAO, Service e Resource mantendo o padrão do projeto"*
  - *"Adicionar funcionalidade mantendo 100% de cobertura de testes e padrões SonarQube"*

---

## 1. Fase 1: Reconhecimento do Projeto Existente

Antes de criar qualquer arquivo, o agente **DEVE INSPECIONAR** o workspace atual para descobrir as convenções adotadas:

1. **Leitura do `pom.xml`**:
   - Identificar o `groupId` (ex: `br.com.imac.siabe` ou `br.com.imac.<projeto>`).
   - Identificar o `artifactId` (ex: `siabe-micro` ou `<projeto>-micro`).
   - Identificar a versão do Java configurada em `<maven.compiler.release>` (ex: `21`, `24`, `17`).
   - Identificar dependências e extensões Quarkus presentes (OIDC, Panache, DB2, OpenAPI, etc.).

2. **Detecção do Pacote Base**:
   - Mapear a pasta de código-fonte: `src/main/java/br/com/imac/<projeto>/api` (ou conforme convenção do projeto).
   - Mapear a pasta de testes: `src/test/java/br/com/imac/<projeto>/api` (ou conforme convenção do projeto).

3. **Inspeção das Configurações (`src/main/resources/application.properties`)**:
   - Porta HTTP configurada (`quarkus.http.port`).
   - Schema padrão de banco (`currentSchema`).
   - Tipo de banco de dados (`db2`, `postgresql`, etc.).

---

## 2. Fase 2: Coleta Interativa dos Requisitos da Funcionalidade

Se o usuário forneceu apenas uma instrução genérica (ex: *"Crie uma nova funcionalidade"* ou *"Adicione a consulta de cliente"*), o agente **DEVE PERGUNTAR** (via `vscode_askQuestions` ou diretamente no chat):

1. **Nome do Domínio / Recurso**: (Ex.: `Beneficiario`, `Contrato`, `Proposta`, `Pagamento`).
2. **Tipo de Operação**:
   - Consulta (GET) com filtros (QueryParam ou PathParam).
   - Inclusão / Envio (POST) com corpo JSON (DTO).
   - Atualização (PUT / PATCH).
   - Exclusão / Cancelamento (DELETE).
3. **Parâmetros e Regras de Validação**:
   - Campos obrigatórios, tamanhos, limites mínimos/máximos, expressões regulares.
4. **Fonte de Dados / Persistência**:
   - Native query SQL via `EntityManager` (padrão legado Caixa / DB2).
   - Panache Entity ou Panache Repository.
   - Chamada externa ou processamento em memória.

Se o usuário já forneceu essas informações detalhadamente no prompt inicial, confirme os artefatos a serem criados e prossiga para a implementação.

---

## 3. Fase 3: Implementação Incremental em Camadas

A nova funcionalidade deve ser construída respeitando a arquitetura em camadas do projeto:

### 3.1. Camada DTO (`br.com.imac.<projeto>.api.dto`)
- Crie Java Records imutáveis para requests e responses:
  - Ex: `<Nome>Request.java`, `<Nome>Response.java`.
- Aplique anotações de Bean Validation (`jakarta.validation.constraints.*`):
  - `@NotNull`, `@NotBlank`, `@Size`, `@Min`, `@Max`, `@Pattern`.

### 3.2. Camada Model / Mapper (`br.com.imac.<projeto>.api.domain.model`)
- Se houver mapeamento de resultado de native query (`Object[]`), crie a classe/registro de mapeamento:
  - Ex: `<Nome>Mapper.java` com método estático de conversão limpo e seguro contra nulos.
- Se for entidade JPA gerenciada, crie a classe anotada com `@Entity` e `@Table(schema = "...", name = "...")`.

### 3.3. Camada DAO / Repositório (`br.com.imac.<projeto>.api.domain.dao`)
- Crie `<Nome>Dao.java` anotado com `@ApplicationScoped`.
- Injete `EntityManager em`.
- Para queries nativas:
  - Utilize parâmetros nomeados (`:parametro`) para prevenir SQL Injection.
  - Utilize constantes em `utils/` para strings de SQL muito longas ou reutilizáveis, evitando alertas de duplicação do SonarQube.
  - Configure limites máximos de resultados (`.setMaxResults(...)`).

### 3.4. Camada Service (`br.com.imac.<projeto>.api.domain.service`)
- Crie `<Nome>Service.java` anotado com `@ApplicationScoped`.
- Injete o DAO correspondente.
- Anote métodos de gravação/alteração com `@Transactional`.
- Encapsule o retorno no envelope padrão `ApiResponse<T>`:
  - Retornar `ApiResponse.of(ResultadoConsulta.SUCESSO, "Mensagem de sucesso", lista)` quando houver dados.
  - Retornar `ApiResponse.of(ResultadoConsulta.NAO_LOCALIZADO, "Nenhum registro encontrado", lista)` quando a lista estiver vazia.
  - Lançar exceções de negócio tratadas quando aplicável.

### 3.5. Camada Resource (`br.com.imac.<projeto>.api.resource`)
- Crie `<Nome>Resource.java` com as anotações JAX-RS / Quarkus REST:
  - `@Path("/api/<recurso>")`
  - `@Produces(MediaType.APPLICATION_JSON)`
  - `@Consumes(MediaType.APPLICATION_JSON)` (se receber body)
  - Anotações OpenAPI: `@Tag`, `@Operation`, `@APIResponses`, `@Parameter`.
  - Injeção do Service correspondente.
- **Padrão Obrigatório de Test Seam (para 100% de cobertura)**:
  - Inclua o endpoint de liveness/health local:
    ```java
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
    ```
  - Isso garante que o bloco `catch` do Resource possa ser coberto no teste unitário através de uma subclasse sem necessidade de reflection frágil.

### 3.6. Regras de Qualidade Sonar (Classes Java Criadas ou Alteradas)
Para evitar apontamentos do SonarQube na etapa de deploy, todo código Java criado ou alterado (principal e de teste) deve respeitar:

- **Operador ternário aninhado (regra "Extract this nested ternary operation into an independent statement")**: nunca usar um `? :` dentro de outro `? :`, na condição, no resultado verdadeiro ou no falso. Extrair a lógica interna para uma variável local, para `if/else` ou para um método privado com nome descritivo.
  - Ternários simples (um único `? :` por expressão) continuam permitidos.
  - Antes de aninhar, verificar se o ternário interno é redundante. Expressões como `x != null ? x : null` equivalem apenas a `x`.
  - Exemplo incorreto:
    ```java
    String mensagemFinal = mensagemAviso != null ? mensagemAviso : (rejeicao != null ? rejeicao : null);
    ```
  - Exemplo correto (ternário interno redundante removido):
    ```java
    String mensagemFinal = mensagemAviso != null ? mensagemAviso : rejeicao;
    ```
  - Exemplo correto (lógica interna realmente necessária, extraída para método privado com `if`):
    ```java
    String cpfFormatado = formatarCpf(cpf, dvCpf);

    private String formatarCpf(Long cpf, Integer dvCpf) {
        if (cpf == null) {
            return null;
        }
        if (dvCpf == null) {
            return String.format("%09d", cpf);
        }
        return String.format("%09d%02d", cpf, dvCpf);
    }
    ```
  - Cada ramificação extraída deve ser coberta por teste unitário, mantendo os 100% de cobertura.
  - Antes de finalizar uma classe, procurar ternários aninhados (regex `\?[^:;\n]*\?[^;\n]*:|:[^;\n]*\?[^;\n]*:` e também expressões em várias linhas) e eliminá-los.
- **Reutilizar constante já definida (regra "Use already-defined constant 'X' instead of duplicating its value here")**: se a classe já declara uma constante com determinado valor (ex.: `CPF_BASE = "123456789"`), nenhum outro trecho da mesma classe pode repetir esse valor literal. Isso vale também para código adicionado depois, como um novo método de teste ou um novo helper.
  - Antes de escrever um literal em uma classe, verificar as constantes `private static final` já declaradas no topo e usar a existente.
  - A regra vale para qualquer tipo de literal (String, números), inclusive em `assertEquals(...)` e em chamadas de métodos.
  - Ao adicionar um teste a uma classe existente, reler as constantes do topo da classe antes de criar massa de dados nova.
  - Exemplo incorreto (a classe de teste já declara `CPF_BASE = "123456789"`):
    ```java
    @Test
    void deveFormatarCpfDoProcuradorSemDvOuSemCpf() {
        assertNull(consultarProcuradorComLinha(new Object[]{"SEM CPF", null, null}).cpf());
        assertEquals("123456789", consultarProcuradorComLinha(new Object[]{"SEM DV", 123456789, null}).cpf());
    }
    ```
  - Exemplo correto:
    ```java
    @Test
    void deveFormatarCpfDoProcuradorSemDvOuSemCpf() {
        assertNull(consultarProcuradorComLinha(new Object[]{"SEM CPF", null, null}).cpf());
        assertEquals(CPF_BASE, consultarProcuradorComLinha(new Object[]{"SEM DV", 123456789, null}).cpf());
    }
    ```
  - Para detectar, listar as constantes da classe (`private static final`) e buscar o valor de cada uma no restante do arquivo; qualquer ocorrência fora da declaração deve ser trocada pela constante.

---

## 4. Fase 4: Implementação da Suíte de Testes (100% de Cobertura)

Nenhuma funcionalidade é considerada pronta sem a criação dos seus respectivos testes em `src/test/java/br/com/imac/<projeto>/api`:

1. **Testes do Service (`<Nome>ServiceTest.java`)**:
   - Cenário com dados retornados (validação de `ResultadoConsulta.SUCESSO` e integridade da lista).
   - Cenário com lista vazia (validação de `ResultadoConsulta.NAO_LOCALIZADO`).
   - Cenários de erro/exceção (se o serviço possuir validações de negócio).

2. **Testes do Resource (`<Nome>ResourceTest.java`)**:
   - Teste de chamada com sucesso (`200 OK`).
   - Teste de chamada com validação com erro (`400 Bad Request`) quando aplicável.
   - Teste do método `health()` retornando sucesso (`200 OK`).
   - Teste do método `health()` sobrescrevendo `registrarHealth(...)` para lançar `RuntimeException` garantindo a cobertura da branch de erro `500 Internal Server Error`.

3. **Testes de Mappers / DTOs (`<Nome>MapperTest.java`)**:
   - Validação da conversão correta de campos, formatos de data/hora, valores nulos e casos de borda.

---

## 5. Fase 5: Atualização da Coleção Postman

Sempre adicione o novo endpoint na coleção existente em `postman/<PROJETO>.postman_collection.json`:
- Criar a nova requisição sob o item correspondente.
- Configurar o método HTTP, rota (`{{baseUrl}}/api/<recurso>/...`), headers (`Accept`, `Content-Type`) e exemplo de corpo (JSON) ou parâmetros de query.

---

## 6. Fase 6: Ciclo de Validação e Execução Obrigatório

Seguindo as diretrizes de ciclo de vida do projeto:
> **Regra Obrigatória**: Após qualquer alteração ou adição de código, executar build/testes, reiniciar a aplicação e validar o endpoint afetado e o health check.

Execute os passos sequencialmente via terminal:

1. **Executar Build e Testes**:
   ```powershell
   .\mvnw.cmd clean test
   ```
   *Certifique-se de que todos os testes passaram e o relatório do JaCoCo foi gerado.*

2. **Reiniciar a Aplicação**:
   ```powershell
   .\start.ps1
   ```
   *O script encerrará o processo anterior pelo arquivo `.pid`, recompilará se necessário, iniciará o processo em background e aguardará o endpoint `/q/health/live` responder com HTTP 200.*

3. **Validar o Novo Endpoint**:
   - Executar chamada de teste (via PowerShell `Invoke-RestMethod` ou similar) contra o endpoint criado para certificar que está respondendo corretamente.

---

## Recursos e Referências

- [Checklist e Padrões de Implementação Incremental](./references/checklist-implementacao.md)
