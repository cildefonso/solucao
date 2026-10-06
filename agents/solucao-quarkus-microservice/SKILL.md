---
name: solucao-quarkus-microservice
description: 'Cria dinamicamente a estrutura de desenvolvimento de novos projetos de microsserviços Java com Quarkus corporativo baseado na arquitetura de referência do SIABE-micro. Solicita interativamente ao usuário o nome desejado do projeto, a versão do Java (ex: 21 LTS, 24 ou 17) e o prefixo do pacote corporativo (ex: br.com.imac.), substituindo todas as ocorrências de SIABE-micro e SIABE (pacotes ${PACKAGE_PREFIX}.${PROJECT_ID}.api, artifactId, schemas de banco, OIDC, scripts start.ps1 com PIDs/logs customizados e cobertura de testes 100%).'
argument-hint: 'Nome do projeto (ex: SICLI-micro), versão do Java (ex: 21, 24, 17) e prefixo do pacote (ex: br.com.imac.)'
user-invocable: true
---

# Scaffold Dinâmico de Microsserviço Quarkus (Baseado em SIABE-micro)

Esta skill guia e automatiza a criação interativa e dinâmica da estrutura completa de desenvolvimento de um novo microsserviço Java com **Quarkus 3.30+**, orientado aos padrões corporativos.

Ela utiliza como modelo de referência arquitetural e de qualidade o **`SIABE-micro`**, **solicitando dinamicamente ao usuário o nome do novo projeto, a versão do Java e o prefixo do pacote corporativo (ex: `br.com.imac.`)**, parametrizando e substituindo todas as ocorrências de `SIABE-micro` / `SIABE`.

---

## Quando Utilizar Esta Skill

- Quando o usuário solicitar:
  - *"Criar estrutura de desenvolvimento de projeto"*
  - *"Criar novo microsserviço baseado no siabe-micro"*
  - *"Scaffold dinâmico de projeto Quarkus"*
  - *"Novo projeto Java (21, 24, etc.) com camadas Resource, Service, DAO, DTO, ApiResponse"*
  - *"Gerar esqueleto de projeto substituindo o nome SIABE-micro"*

---

## 1. Passo Inicial Obrigatório: Coleta Interativa (Nome, Versão do Java e Prefixo de Pacote)

Antes de gerar qualquer arquivo ou pasta, o agente **DEVE OBRIGATORIAMENTE** verificar se o usuário já forneceu:
1. **Nome ou sigla do projeto** (ex: `SICLI-micro`, `SIASG-micro`).
2. **Versão do Java** (ex: `21` [LTS corporativo], `24` [referência do SIABE-micro], `17` [LTS]).
3. **Prefixo do Pacote Corporativo / GroupId Base** (ex: `br.com.imac.` ou `br.com.imac`). O agente **DEVE SOLICITAR EXPLICITAMENTE** esse valor para o usuário, sugerindo `br.com.imac.` como padrão para confirmação ou alteração.

### Regra de Interação:
- Se qualquer uma dessas informações **NÃO** tiver sido especificada pelo usuário no prompt inicial:
  - O agente **DEVE PERGUNTAR** ao usuário antes de prosseguir, utilizando a ferramenta `vscode_askQuestions` (se disponível) ou mensagem direta no chat.
  - As perguntas a apresentar:
    1. **Nome do Projeto**: "Qual é o nome ou sigla do novo microsserviço? (ex.: SICLI-micro, SIASG-micro, SIGLA-micro)"
    2. **Versão do Java**: "Qual versão do Java você deseja utilizar no projeto?"
       - Opções sugeridas:
         - `21` (LTS recomendada para produção corporativa)
         - `24` (Versão de referência do SIABE-micro)
         - `17` (LTS legado)
    3. **Prefixo do Pacote Corporativo**: "Qual é o prefixo de pacote corporativo? (padrão sugerido: `br.com.imac.`)"
       - *Tratamento de formatação*: Se informado com ponto final (`br.com.imac.`), o ponto final pode ser preservado ou removido para compor `${PACKAGE_PREFIX}` normalizado (ex: `br.com.imac`).
    4. *(Opcional)* **Porta HTTP**: Padrão `8080` (ou customizada).
    5. *(Opcional)* **Banco de Dados**: `DB2` (padrão legado Caixa), `PostgreSQL` ou `Oracle`.

- Se o usuário já tiver informado os parâmetros (ex: *"Crie o projeto SICLI-micro em Java 21 com pacote br.com.imac."*):
  - Confirme os parâmetros derivados e prossiga diretamente para a geração da estrutura.

---

## 2. Tabela de Derivação e Substituição Dinâmica

A partir dos dados fornecidos pelo usuário, calcule as variáveis e execute as substituições em todos os pontos onde o modelo original possui referências ao `SIABE-micro` / `SIABE`, à versão do Java e ao pacote corporativo:

| Conceito | Variável Derivada | Modelo Original (SIABE-micro) | Novo Projeto (Exemplo: SICLI em Java 21 com `br.com.imac.`) |
|---|---|---|---|
| **Nome Base do Projeto** | `${PROJECT_NAME}` | `SIABE-micro` | `SICLI-micro` |
| **Versão do Java** | `${JAVA_VERSION}` | `24` | `21` (ou a versão escolhida pelo usuário) |
| **Prefixo do Pacote** | `${PACKAGE_PREFIX}` | `br.com.imac` | `br.com.imac` (valor solicitado e confirmado com o usuário) |
| **Caminho do Pacote** | `${PACKAGE_PATH}` | `br/com/imac` | Caminho derivado de `${PACKAGE_PREFIX}` (ex: `br/com/imac`) |
| **Identificador / Sigla (minúsculo)** | `${PROJECT_ID}` | `siabe` | `sicli` |
| **Identificador / Sigla (maiúsculo)** | `${PROJECT_UPPER}` | `SIABE` | `SICLI` |
| **ArtifactId Maven** | `${ARTIFACT_ID}` | `siabe-micro` | `${PROJECT_ID}-micro` (ex: `sicli-micro`) |
| **GroupId Maven** | `${GROUP_ID}` | `br.com.imac.xpto` | `${PACKAGE_PREFIX}.${PROJECT_ID}` |
| **Pacote Base Java** | `${BASE_PACKAGE}` | `br.com.imac.xpto.api` | `${PACKAGE_PREFIX}.${PROJECT_ID}.api` |
| **Diretório Código-Fonte** | `${SRC_JAVA_DIR}` | `src/main/java/br/com/imac/xpto/api` | `src/main/java/${PACKAGE_PATH}/${PROJECT_ID}/api` |
| **Diretório Testes** | `${TEST_JAVA_DIR}` | `src/test/java/br/com/imac/xpto/api` | `src/test/java/${PACKAGE_PATH}/${PROJECT_ID}/api` |
| **Release do Compilador Java** | `${MAVEN_COMPILER_RELEASE}` | `24` | `${JAVA_VERSION}` (ex: `21`) |
| **Schema do Banco de Dados** | `${DB_SCHEMA}` | `SIABE` | `${PROJECT_UPPER}` |
| **Client ID OIDC** | `${OIDC_CLIENT_ID}` | `cli-web-abe` | `cli-web-${PROJECT_ID}` |
| **Arquivo PID da Aplicação** | `${PID_FILE}` | `.siabe-backend.pid` | `.${PROJECT_ID}-backend.pid` |
| **Arquivo Log de Saída** | `${OUT_LOG_FILE}` | `.siabe-backend.out.log` | `.${PROJECT_ID}-backend.out.log` |
| **Arquivo Log de Erro** | `${ERR_LOG_FILE}` | `.siabe-backend.err.log` | `.${PROJECT_ID}-backend.err.log` |
| **Coleção Postman** | `${POSTMAN_FILE}` | `postman/SIABE-DATAPREV.postman_collection.json` | `postman/${PROJECT_UPPER}.postman_collection.json` |
| **Título do README** | `${README_TITLE}` | `# SIABE Backend API` | `# ${PROJECT_UPPER} Backend API (Java ${JAVA_VERSION})` |

---

## 3. Estrutura Canônica de Diretórios Gerada

Ao executar a criação, crie a seguinte estrutura com o pacote e arquivos parametrizados para `${PACKAGE_PATH}` e `${PROJECT_ID}`:

```text
<diretório-do-projeto>/
├── .mvn/
│   └── wrapper/
│       ├── maven-wrapper.jar
│       └── maven-wrapper.properties
├── postman/
│   └── ${PROJECT_UPPER}.postman_collection.json
├── src/
│   ├── main/
│   │   ├── java/${PACKAGE_PATH}/${PROJECT_ID}/api/
│   │   │   ├── domain/
│   │   │   │   ├── dao/                 # DAOs com native query / EntityManager
│   │   │   │   ├── exception/           # ExceptionMappers JAX-RS customizados
│   │   │   │   ├── model/               # Entidades JPA, registros de banco e Mappers
│   │   │   │   └── service/             # Regras de negócio e transações (@Transactional)
│   │   │   ├── dto/                     # Records Java imutáveis (Request/Response)
│   │   │   ├── enums/                   # Enums (ResultadoConsulta)
│   │   │   ├── resource/                # Endpoints REST (JAX-RS + OpenAPI + Test Seams)
│   │   │   ├── retorno/                 # Envelope padrão ApiResponse<T>
│   │   │   └── utils/                   # Constantes corporativas e utilitários
│   │   └── resources/
│   │       ├── application.properties
│   │       └── application-local.properties
│   └── test/
│       └── java/${PACKAGE_PATH}/${PROJECT_ID}/api/
│           ├── domain/
│           │   ├── exception/           # Testes de ExceptionMappers (100% cobertura)
│           │   ├── model/               # Testes de Mappers de domínio
│           │   └── service/             # Testes unitários com stubs/mocks
│           ├── resource/                # Testes de Resource (sucesso e falhas via seam)
│           └── retorno/                 # Teste do envelope ApiResponse
├── .dockerignore
├── .gitignore
├── Dockerfile
├── mvnw
├── mvnw.cmd
├── pom.xml
├── README.md
└── start.ps1
```

---

## 4. Passo a Passo de Implementação dos Arquivos

### 4.1. `pom.xml` Dinâmico
- Configurar:
  - `<groupId>${PACKAGE_PREFIX}.${PROJECT_ID}</groupId>`
  - `<artifactId>${PROJECT_ID}-micro</artifactId>`
  - `<name>${PROJECT_NAME}</name>`
  - `<maven.compiler.release>${JAVA_VERSION}</maven.compiler.release>`
- Dependências essenciais:
  - Quarkus BOM `3.30.5` (compatível com Java 17, 21 e 24)
  - `quarkus-rest-jackson`
  - `quarkus-oidc`
  - `quarkus-hibernate-orm-panache`
  - `quarkus-jdbc-db2` (ou driver correspondente ao banco escolhido)
  - `quarkus-smallrye-openapi`
  - `quarkus-smallrye-health`
  - `jacoco-maven-plugin` 0.8.13+
- Referência: [pom-template.xml](./references/pom-template.xml).

### 4.2. `src/main/resources/application.properties` Dinâmico
- Configurações com substituição direta:
  ```properties
  quarkus.http.port=8080
  quarkus.resteasy.path=/api
  quarkus.transaction-manager.default-transaction-timeout=PT60M

  # OIDC
  quarkus.oidc.auth-server-url=https://login.des.caixa/auth/realms/intranet
  quarkus.oidc.client-id=cli-web-${PROJECT_ID}
  quarkus.oidc.credentials.secret=secret
  quarkus.oidc.application-type=service
  quarkus.oidc.roles.source=accesstoken
  quarkus.oidc.token.auto-refresh-interval=18000

  quarkus.http.auth.permission.authenticated.paths=/api/*
  quarkus.http.auth.permission.authenticated.policy=authenticated

  # Datasource
  quarkus.datasource.db-kind=db2
  quarkus.datasource.username=${DB_USER:usuario}
  quarkus.datasource.password=${DB_PASSWORD:senha}
  quarkus.datasource.jdbc.url=jdbc:db2://localhost:50000/DB:currentSchema=${PROJECT_UPPER};
  quarkus.hibernate-orm.packages=${PACKAGE_PREFIX}.${PROJECT_ID}.api.domain.model
  quarkus.hibernate-orm.dialect=org.hibernate.dialect.DB2Dialect
  quarkus.datasource.jdbc.driver=com.ibm.db2.jcc.DB2Driver
  quarkus.datasource.jdbc.max-size=40

  # Logs
  quarkus.log.level=INFO
  quarkus.log.category."${PACKAGE_PREFIX}.${PROJECT_ID}".level=DEBUG
  ```
- Referência: [application-properties.template](./references/application-properties.template).

### 4.3. Classes Java Dinâmicas (com Pacote `${PACKAGE_PREFIX}.${PROJECT_ID}.api`)
Consulte o [Guia de Arquitetura](./references/architecture-guide.md):
1. **`ApiResponse<T>`**: Em `${PACKAGE_PREFIX}.${PROJECT_ID}.api.retorno`.
2. **`ResultadoConsulta`**: Em `${PACKAGE_PREFIX}.${PROJECT_ID}.api.enums`.
3. **`ExceptionMappers`**: Em `${PACKAGE_PREFIX}.${PROJECT_ID}.api.domain.exception`.
4. **`Resource` com Test Seam**: Em `${PACKAGE_PREFIX}.${PROJECT_ID}.api.resource`, incluindo o método `void registrarHealth(String status)` para permitir teste de falhas sem reflection.

### 4.4. Script de Ciclo de Vida Local (`start.ps1`) Dinâmico
- Parametrizar a verificação de versão do Java de acordo com `${JAVA_VERSION}`:
  ```powershell
  $projectRoot = $PSScriptRoot
  $pidFile = Join-Path $projectRoot '.${PROJECT_ID}-backend.pid'
  $outputLogFile = Join-Path $projectRoot '.${PROJECT_ID}-backend.out.log'
  $errorLogFile = Join-Path $projectRoot '.${PROJECT_ID}-backend.err.log'
  $runnerJar = Join-Path $projectRoot 'target\quarkus-app\quarkus-run.jar'
  $applicationDat = Join-Path $projectRoot 'target\quarkus-app\quarkus\quarkus-application.dat'
  $applicationProperties = Join-Path $projectRoot 'src\main\resources\application.properties'
  $mavenWrapper = Join-Path $projectRoot 'mvnw.cmd'

  if (-not $env:JAVA_HOME) {
      $defaultJavaHome = 'C:\caixa\software\jdk-${JAVA_VERSION}'
      if (-not (Test-Path $defaultJavaHome)) {
          # Tenta localizar JDK com a versão escolhida
          $found = Get-ChildItem 'C:\caixa\software' -Filter "jdk-${JAVA_VERSION}*" -Directory -ErrorAction SilentlyContinue | Select-Object -First 1
          if ($found) { $defaultJavaHome = $found.FullName }
      }
      if (Test-Path $defaultJavaHome) {
          $env:JAVA_HOME = $defaultJavaHome
      } else {
          throw "JAVA_HOME não definido. Configure-o para um JDK ${JAVA_VERSION} antes de iniciar a aplicação."
      }
  }
  ```
- Referência: [lifecycle-script.ps1](./references/lifecycle-script.ps1).

### 4.5. `.gitignore` Dinâmico e Completo
O arquivo `.gitignore` deve cobrir **todos** os arquivos e pastas que não devem subir para o repositório Git, organizados por categorias:
- **Build & Maven**: `target/`, `.mvn/wrapper/maven-wrapper.jar`, `pom.xml.tag`, `release.properties`, etc.
- **Logs & Processos Locais**: `*.log`, `.${PROJECT_ID}-backend.pid`, `.${PROJECT_ID}-backend.out.log`, `.${PROJECT_ID}-backend.err.log`, `start.ps1`.
- **Configurações Locais & Segredos**: `application-local.properties`, `.env*`, `credentials.json`, etc.
- **IDEs & Editores**: `.idea/`, `*.iml`, `.vscode/*` (preservando configurações úteis se houver), `.settings/`, `.classpath`, `.project`, `*.code-workspace`.
- **Sistema Operacional**: `Thumbs.db`, `Desktop.ini`, `.DS_Store`, etc.
- **Assistentes & Temporários**: `tmp/`, `.agents/`, `.claude/`, `.solucao/`, `AGENTS.md`, `CLAUDE.md`, `_${PROJECT_ID}_sdd/`.
- Referência completa: [gitignore.template](./references/gitignore.template).

### 4.6. `README.md` Dinâmico
- Gerar o README com o título `# ${PROJECT_UPPER} Backend API (Java ${JAVA_VERSION})`, pré-requisito de JDK `${JAVA_VERSION}`, comandos de build com Maven Wrapper (`./mvnw.cmd clean package`), execução com `./start.ps1` e endpoints de documentação (`/q/swagger-ui`, `/q/openapi`, `/q/health`).

### 4.7. Regras de Qualidade Sonar (Obrigatórias nas Classes Geradas)
Para evitar apontamentos do SonarQube na etapa de deploy, todo código Java gerado deve respeitar:

- **Literais String duplicados (regra "Define a constant instead of duplicating this literal \"X\" N times")**: qualquer literal String usado 3 ou mais vezes na mesma classe deve ser extraído para uma constante `private static final String`, nomeada em `UPPER_SNAKE_CASE`. Isso vale principalmente para nomes de parâmetros de `Query` (`.setParameter("beneficio", ...)`), chaves de mapas, mensagens e códigos de situação.
  - Convenção de nomes: `PARAM_<NOME>` para parâmetros de query (ex.: `PARAM_BENEFICIO`, `PARAM_NIT`, `PARAM_PV`, `PARAM_CONTA`); `MSG_<NOME>` para mensagens; `SIT_<NOME>` para códigos de situação.
  - A constante deve ficar no topo da classe, antes dos campos injetados.
  - A mesma constante deve ser usada em todos os `setParameter` do mesmo nome, mas o nome dentro do SQL (`:beneficio`) continua literal, pois está dentro do text block.
  - Exemplo incorreto:
    ```java
    List<Object[]> rows = entityManager.createNativeQuery(sql)
            .setParameter("beneficio", numeroBeneficio)
            .getResultList();
    // ... mais 5 métodos repetindo .setParameter("beneficio", ...)
    ```
  - Exemplo correto:
    ```java
    @ApplicationScoped
    public class BeneficioContaDao {

        private static final String PARAM_BENEFICIO = "beneficio";

        // ...
        List<Object[]> rows = entityManager.createNativeQuery(sql)
                .setParameter(PARAM_BENEFICIO, numeroBeneficio)
                .getResultList();
    }
    ```
  - **Classes de teste (`*Test.java`)**: a regra vale também para os testes gerados. Valores de massa de teste repetidos (CPF, NIT, nomes, mensagens esperadas, valores monetários como `"500.00"`) usados 3 ou mais vezes na mesma classe, inclusive em `assertEquals(...)` e nas chamadas ao método testado, devem virar constantes `private static final String` no topo da classe de teste. Classes internas estáticas e classes anônimas (stubs/fakes) acessam as constantes da classe externa.
    - Convenção de nomes: `CPF_VALIDO`, `CPF_BASE`, `VALOR_<NOME>`, `COMPETENCIA_<NOME>`, `MSG_<NOME>`.
    - Exemplo incorreto (Sonar: `Define a constant instead of duplicating this literal "12345678901" 4 times`):
      ```java
      resource.extratoPagamentoService = new ExtratoPagamentoService() {
          @Override
          public ApiResponse<ExtratoPagamentoResponse> consultar(Long beneficio, String cpf, LocalDate dataReferencia) {
              assertEquals(987654L, beneficio);
              assertEquals("12345678901", cpf);
              // ...
          }
      };
      var response = resource.consultar(987654L, "12345678901", referencia);
      ```
    - Exemplo correto:
      ```java
      class ResourceTest {

          private static final String CPF_VALIDO = "12345678901";

          // ...
          assertEquals(CPF_VALIDO, cpf);
          var response = resource.consultar(987654L, CPF_VALIDO, referencia);
      }
      ```
  - Antes de finalizar uma classe (principal ou de teste), revisar se algum literal se repete 3 ou mais vezes e, se houver, extrair a constante. Para listar candidatos, agrupar os literais do arquivo (regex `"[^"\r\n]{4,}"`) e tratar todos com contagem maior ou igual a 3, não apenas o apontado pelo Sonar.
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

## 5. Validação Pós-Criação

Após gerar a estrutura dinâmica:
1. Executar a suíte de testes unitários:
   ```powershell
   .\mvnw.cmd clean package
   ```
2. Iniciar a aplicação e verificar a saúde no endpoint `/q/health/live`:
   ```powershell
   .\start.ps1
   ```
3. Garantir 100% de cobertura nos testes e ausência de literais duplicados (constantes `private static final String` para qualquer literal repetido 3 ou mais vezes, conforme a seção 4.7) para conformidade no SonarQube.

---

## Recursos e Referências

- [Guia Detalhado de Arquitetura](./references/architecture-guide.md)
- [Template Dinâmico de pom.xml](./references/pom-template.xml)
- [Template Dinâmico de application.properties](./references/application-properties.template)
- [Template Dinâmico de start.ps1](./references/lifecycle-script.ps1)
- [Template Dinâmico de .gitignore](./references/gitignore.template)
