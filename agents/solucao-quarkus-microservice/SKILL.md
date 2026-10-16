---
name: solucao-quarkus-microservice
description: 'Cria dinamicamente a estrutura de desenvolvimento de novos projetos de microsserviços Java com Quarkus corporativo baseado na arquitetura de referência do XPTO-BACKEND. Solicita interativamente ao usuário o nome desejado do projeto, a versão do Java (ex: 21 LTS, 24 ou 17), o prefixo do pacote corporativo (ex: br.com.imac.), a porta HTTP (quarkus.http.port, ex: 8083), a URL do servidor OIDC (quarkus.oidc.auth-server-url), a secret do client OIDC (quarkus.oidc.credentials.secret), a URL JDBC do banco (quarkus.datasource.jdbc.url), o dialect do Hibernate (quarkus.hibernate-orm.dialect) o driver JDBC (quarkus.datasource.jdbc.driver) e o caminho da JDK local (JAVA_HOME), substituindo todas as ocorrências de XPTO-BACKEND e XPTO (pacotes ${PACKAGE_PREFIX}.${PROJECT_ID}.api, artifactId, schemas de banco, OIDC, scripts start.ps1 com PIDs/logs customizados e cobertura de testes 100%).'
argument-hint: 'Nome do projeto (ex: XPTO-BACKEND), versão do Java (ex: 21, 24, 17), prefixo do pacote (ex: br.com.imac.), porta HTTP (ex: 8083), URL OIDC (ex: https://www.des.xpto/auth/realms/intranet), secret OIDC, URL JDBC (ex: jdbc:postgresql://host:5432/BANCO:currentSchema=SCHEMA;), dialect Hibernate (ex: org.hibernate.dialect.PostgreSQLDialect), driver JDBC (ex: org.postgresql.Driver) e caminho da JDK (ex: C:\\software\\jdk-21)'
user-invocable: true
---

# Scaffold Dinâmico de Microsserviço Quarkus (Baseado em XPTO-BACKEND)

Esta skill guia e automatiza a criação interativa e dinâmica da estrutura completa de desenvolvimento de um novo microsserviço Java com **Quarkus 3.30+**, orientado aos padrões corporativos.

Ela utiliza como modelo de referência arquitetural e de qualidade o **`XPTO-BACKEND`**, **solicitando dinamicamente ao usuário o nome do novo projeto, a versão do Java e o prefixo do pacote corporativo (ex: `br.com.imac.`)**, parametrizando e substituindo todas as ocorrências de `XPTO-BACKEND` / `XPTO`.

---

## Quando Utilizar Esta Skill

- Quando o usuário solicitar:
  - *"Criar estrutura de desenvolvimento de projeto"*
  - *"Criar novo microsserviço baseado no xpto-backend"*
  - *"Scaffold dinâmico de projeto Quarkus"*
  - *"Novo projeto Java (21, 24, etc.) com camadas Resource, Service, DAO, DTO, ApiResponse"*
  - *"Gerar esqueleto de projeto substituindo o nome XPTO-BACKEND"*

---

## 1. Passo Inicial Obrigatório: Coleta Interativa (Nome, Versão do Java, Prefixo de Pacote, Porta HTTP, URL OIDC, Secret OIDC, URL JDBC, Dialect, Driver JDBC e Caminho da JDK)

Antes de gerar qualquer arquivo ou pasta, o agente **DEVE OBRIGATORIAMENTE** verificar se o usuário já forneceu:
1. **Nome ou sigla do projeto** (ex: `XPTO-BACKEND`, `SIASG-micro`).
2. **Versão do Java** (ex: `21` [LTS corporativo], `24` [referência do XPTO-BACKEND], `17` [LTS]).
3. **Prefixo do Pacote Corporativo / GroupId Base** (ex: `br.com.imac.` ou `br.com.imac`). O agente **DEVE SOLICITAR EXPLICITAMENTE** esse valor para o usuário, sugerindo `br.com.imac.` como padrão para confirmação ou alteração.
4. **Porta HTTP da aplicação** (`quarkus.http.port`, ex: `8083`). O agente **DEVE SOLICITAR EXPLICITAMENTE** esse valor ao usuário e **NÃO** deve assumir um valor padrão silenciosamente.
5. **URL do servidor OIDC** (`quarkus.oidc.auth-server-url`, ex: `https://www.des.xpto/auth/realms/intranet`). O agente **DEVE SOLICITAR EXPLICITAMENTE** esse valor ao usuário e **NÃO** deve assumir um valor padrão silenciosamente.
6. **Secret do client OIDC** (`quarkus.oidc.credentials.secret`). O agente **DEVE SOLICITAR EXPLICITAMENTE** esse valor ao usuário e **NUNCA** deve reutilizar a secret do XPTO-BACKEND nem inventar um valor.
7. **URL JDBC do banco de dados** (`quarkus.datasource.jdbc.url`, ex: `jdbc:postgresql://host:5432/BANCO:currentSchema=SCHEMA;`). O agente **DEVE SOLICITAR EXPLICITAMENTE** esse valor ao usuário e **NÃO** deve reutilizar o host/porta do XPTO-BACKEND nem assumir um valor padrão silenciosamente.
8. **Dialect do Hibernate ORM** (`quarkus.hibernate-orm.dialect`, ex: `org.hibernate.dialect.PostgreSQLDialect`). O agente **DEVE SOLICITAR EXPLICITAMENTE** esse valor ao usuário e **NÃO** deve assumir um valor padrão silenciosamente.
9. **Driver JDBC** (`quarkus.datasource.jdbc.driver`, ex: `org.postgresql.Driver`). O agente **DEVE SOLICITAR EXPLICITAMENTE** esse valor ao usuário e **NÃO** deve assumir um valor padrão silenciosamente.
10. **Caminho da JDK local** (`JAVA_HOME` usado pelo `start.ps1`, ex: `C:\software\jdk-21`). O agente **DEVE SOLICITAR EXPLICITAMENTE** esse valor ao usuário e **NÃO** deve assumir nenhum diretório fixo (ex.: `C:\caixa\software`) nem tentar descobri-lo silenciosamente.

### Regra de Interação:
- Se qualquer uma dessas informações **NÃO** tiver sido especificada pelo usuário no prompt inicial:
  - O agente **DEVE PERGUNTAR** ao usuário antes de prosseguir, utilizando a ferramenta `vscode_askQuestions` (se disponível) ou mensagem direta no chat.
  - As perguntas a apresentar:
    1. **Nome do Projeto**: "Qual é o nome ou sigla do novo microsserviço? (ex.: XPTO-BACKEND, SIASG-micro, SIGLA-micro)"
    2. **Versão do Java**: "Qual versão do Java você deseja utilizar no projeto?"
       - Opções sugeridas:
         - `21` (LTS recomendada para produção corporativa)
         - `24` (Versão de referência do XPTO-BACKEND)
         - `17` (LTS legado)
    3. **Prefixo do Pacote Corporativo**: "Qual é o prefixo de pacote corporativo? (padrão sugerido: `br.com.imac.`)"
       - *Tratamento de formatação*: Se informado com ponto final (`br.com.imac.`), o ponto final pode ser preservado ou removido para compor `${PACKAGE_PREFIX}` normalizado (ex: `br.com.imac`).
    4. **Porta HTTP (`quarkus.http.port`)**: "Qual porta HTTP a aplicação deve utilizar (propriedade `quarkus.http.port`)? (ex.: 8083)"
       - *Validação*: deve ser um inteiro entre `1024` e `65535`; se inválida, perguntar novamente.
       - O valor informado é usado em `${HTTP_PORT}` no `application.properties` e nas verificações de saúde do `start.ps1`/README.
    5. **URL do servidor OIDC (`quarkus.oidc.auth-server-url`)**: "Qual é a URL do servidor OIDC/Keycloak (propriedade `quarkus.oidc.auth-server-url`)? (ex.: https://www.des.xpto/auth/realms/intranet)"
       - *Validação*: deve ser uma URL `https://` que inclua o realm (`.../auth/realms/<realm>`); se inválida, perguntar novamente.
       - O valor informado é usado em `${OIDC_AUTH_SERVER_URL}` no `application.properties`.
    6. **Secret do client OIDC (`quarkus.oidc.credentials.secret`)**: "Qual é a secret do client OIDC (propriedade `quarkus.oidc.credentials.secret`)? Se preferir não informar agora, responda `ENV` para que ela seja lida da variável de ambiente `OIDC_CLIENT_SECRET`."
       - **Esta pergunta DEVE ser feita por mensagem direta no chat**, nunca pela ferramenta `vscode_askQuestions` (dados sensíveis não devem trafegar por formulários de perguntas).
       - *Validação*: não pode ser vazia; se vazia, perguntar novamente.
       - *Tratamento seguro do valor*:
         - O `application.properties` (versionado) **NUNCA** deve conter a secret literal; ele referencia `quarkus.oidc.credentials.secret=${OIDC_CLIENT_SECRET}`.
         - Se o usuário informou a secret, gravá-la **apenas** em `src/main/resources/application-local.properties` (`quarkus.oidc.credentials.secret=<valor informado>`), arquivo que consta no `.gitignore`.
         - Se o usuário respondeu `ENV`, não gravar nenhum valor; orientar a definir a variável de ambiente `OIDC_CLIENT_SECRET` antes de iniciar a aplicação.
         - **Não** repetir a secret em respostas do chat, README, logs, coleção Postman ou comandos de terminal.
    7. **URL JDBC (`quarkus.datasource.jdbc.url`)**: "Qual é a URL JDBC do banco de dados (propriedade `quarkus.datasource.jdbc.url`)? (ex.: jdbc:postgresql://host:5432/BANCO:currentSchema=SCHEMA;)"
       - *Validação*: deve começar com `jdbc:` e ser compatível com o banco escolhido (`jdbc:db2:`, `jdbc:postgresql:` ou `jdbc:oracle:`); se inválida, perguntar novamente.
       - Se a URL não contiver o schema (`currentSchema=`), perguntar ao usuário se deseja acrescentá-lo (sugerir `${DB_SCHEMA}`) antes de prosseguir.
       - O valor informado é usado em `${JDBC_URL}` no `application.properties`; a URL **não** deve conter usuário nem senha embutidos (ex.: `user=`/`password=`).
    8. **Dialect do Hibernate (`quarkus.hibernate-orm.dialect`)**: "Qual dialect do Hibernate ORM deve ser utilizado (propriedade `quarkus.hibernate-orm.dialect`)?"
       - Opções sugeridas (de acordo com o banco da URL JDBC informada):
         - `org.hibernate.dialect.DB2Dialect` (para `jdbc:db2:`, referência do XPTO-BACKEND)
         - `org.hibernate.dialect.PostgreSQLDialect` (para `jdbc:postgresql:`)
         - `org.hibernate.dialect.OracleDialect` (para `jdbc:oracle:`)
       - *Validação*: deve ser um nome de classe totalmente qualificado (`org.hibernate.dialect.<Nome>Dialect`) e compatível com o banco da URL JDBC; se incompatível, alertar o usuário e perguntar novamente.
       - O valor informado é usado em `${HIBERNATE_DIALECT}` no `application.properties`.
    9. **Driver JDBC (`quarkus.datasource.jdbc.driver`)**: "Qual driver JDBC deve ser utilizado (propriedade `quarkus.datasource.jdbc.driver`)?"
       - Opções sugeridas (de acordo com o banco da URL JDBC informada):
         - `com.ibm.db2.jcc.DB2Driver` (para `jdbc:db2:`, referência do XPTO-BACKEND)
         - `org.postgresql.Driver` (para `jdbc:postgresql:`)
         - `oracle.jdbc.OracleDriver` (para `jdbc:oracle:`)
       - *Validação*: deve ser um nome de classe totalmente qualificado e compatível com o banco da URL JDBC; se incompatível, alertar o usuário e perguntar novamente.
       - O valor informado é usado em `${JDBC_DRIVER}` no `application.properties`; a dependência Quarkus correspondente (`quarkus-jdbc-db2`, `quarkus-jdbc-postgresql` ou `quarkus-jdbc-oracle`) e o `quarkus.datasource.db-kind` (`db2`, `postgresql` ou `oracle`) devem ser coerentes com o driver escolhido.
    10. **Caminho da JDK (`JAVA_HOME`)**: "Qual é o caminho completo da JDK ${JAVA_VERSION} instalada na sua máquina (diretório raiz, que contém `bin\java.exe`)? (ex.: C:\software\jdk-21)"
       - *Validação*: o caminho deve existir e conter `bin\java.exe` (verificar com `Test-Path`); se não existir, informar o usuário e perguntar novamente. Alertar se a versão do JDK informado divergir de `${JAVA_VERSION}`.
       - O valor informado é usado em `${JDK_PATH}` no `start.ps1` e **só é aplicado quando a variável de ambiente `JAVA_HOME` não estiver definida**.
    11. *(Opcional)* **Banco de Dados**: `PostgreSQL` (padrão), `DB2` (legado XPTO) ou `Oracle`.

- Se o usuário já tiver informado os parâmetros (ex: *"Crie o projeto XPTO-BACKEND em Java 21 com pacote br.com.imac."*):
  - Confirme os parâmetros derivados e prossiga diretamente para a geração da estrutura.

---

## 2. Tabela de Derivação e Substituição Dinâmica

A partir dos dados fornecidos pelo usuário, calcule as variáveis e execute as substituições em todos os pontos onde o modelo original possui referências ao `XPTO-BACKEND` / `XPTO`, à versão do Java e ao pacote corporativo:

| Conceito | Variável Derivada | Modelo Original (XPTO-BACKEND) | Novo Projeto (Exemplo: XPTO em Java 21 com `br.com.imac.`) |
|---|---|---|---|
| **Nome Base do Projeto** | `${PROJECT_NAME}` | `XPTO-BACKEND` | `XPTO-BACKEND` |
| **Versão do Java** | `${JAVA_VERSION}` | `24` | `21` (ou a versão escolhida pelo usuário) |
| **Prefixo do Pacote** | `${PACKAGE_PREFIX}` | `br.com.imac` | `br.com.imac` (valor solicitado e confirmado com o usuário) |
| **Porta HTTP** | `${HTTP_PORT}` | `8083` | Valor informado pelo usuário (ex: `8083`) |
| **URL do Servidor OIDC** | `${OIDC_AUTH_SERVER_URL}` | `https://www.des.xpto/auth/realms/intranet` | Valor informado pelo usuário |
| **Secret do Client OIDC** | `${OIDC_CLIENT_SECRET}` | *(não reutilizar a do XPTO-BACKEND)* | Valor informado pelo usuário, gravado somente em `application-local.properties` (ou variável de ambiente `OIDC_CLIENT_SECRET`) |
| **Caminho do Pacote** | `${PACKAGE_PATH}` | `br/com/imac` | Caminho derivado de `${PACKAGE_PREFIX}` (ex: `br/com/imac`) |
| **Identificador / Sigla (minúsculo)** | `${PROJECT_ID}` | `xpto` | `xpto` |
| **Identificador / Sigla (maiúsculo)** | `${PROJECT_UPPER}` | `XPTO` | `XPTO` |
| **ArtifactId Maven** | `${ARTIFACT_ID}` | `xpto-backend` | `${PROJECT_ID}-micro` (ex: `xpto-backend`) |
| **GroupId Maven** | `${GROUP_ID}` | `br.com.imac.xpto` | `${PACKAGE_PREFIX}.${PROJECT_ID}` |
| **Pacote Base Java** | `${BASE_PACKAGE}` | `br.com.imac.xpto.api` | `${PACKAGE_PREFIX}.${PROJECT_ID}.api` |
| **Diretório Código-Fonte** | `${SRC_JAVA_DIR}` | `src/main/java/br/com/imac/xpto/api` | `src/main/java/${PACKAGE_PATH}/${PROJECT_ID}/api` |
| **Diretório Testes** | `${TEST_JAVA_DIR}` | `src/test/java/br/com/imac/xpto/api` | `src/test/java/${PACKAGE_PATH}/${PROJECT_ID}/api` |
| **Release do Compilador Java** | `${MAVEN_COMPILER_RELEASE}` | `24` | `${JAVA_VERSION}` (ex: `21`) |
| **Schema do Banco de Dados** | `${DB_SCHEMA}` | `XPTO` | `${PROJECT_UPPER}` |
| **URL JDBC** | `${JDBC_URL}` | `jdbc:postgresql://HOST:5432/DBD0:currentSchema=XPTO;` | Valor informado pelo usuário |
| **Dialect do Hibernate** | `${HIBERNATE_DIALECT}` | `org.hibernate.dialect.PostgreSQLDialect` | Valor informado pelo usuário |
| **Driver JDBC** | `${JDBC_DRIVER}` | `org.postgresql.Driver` | Valor informado pelo usuário |
| **Caminho da JDK** | `${JDK_PATH}` | *(não reutilizar caminho fixo)* | Valor informado pelo usuário (ex: `C:\software\jdk-21`) |
| **Client ID OIDC** | `${OIDC_CLIENT_ID}` | `cli-web-xpto` | `cli-web-${PROJECT_ID}` |
| **Arquivo PID da Aplicação** | `${PID_FILE}` | `.xpto-backend.pid` | `.${PROJECT_ID}-backend.pid` |
| **Arquivo Log de Saída** | `${OUT_LOG_FILE}` | `.xpto-backend.out.log` | `.${PROJECT_ID}-backend.out.log` |
| **Arquivo Log de Erro** | `${ERR_LOG_FILE}` | `.xpto-backend.err.log` | `.${PROJECT_ID}-backend.err.log` |
| **Coleção Postman** | `${POSTMAN_FILE}` | `postman/XPTO-DATAPREV.postman_collection.json` | `postman/${PROJECT_UPPER}.postman_collection.json` |
| **Título do README** | `${README_TITLE}` | `# XPTO Backend API` | `# ${PROJECT_UPPER} Backend API (Java ${JAVA_VERSION})` |

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
  - `quarkus-jdbc-postgresql` (ou driver correspondente ao banco escolhido)
  - `quarkus-smallrye-openapi`
  - `quarkus-smallrye-health`
  - `jacoco-maven-plugin` 0.8.13+
- Referência: [pom-template.xml](./references/pom-template.xml).

### 4.2. `src/main/resources/application.properties` Dinâmico
- Configurações com substituição direta:
  ```properties
  quarkus.http.port=${HTTP_PORT}
  quarkus.resteasy.path=/api
  quarkus.transaction-manager.default-transaction-timeout=PT60M

  # OIDC
  quarkus.oidc.auth-server-url=${OIDC_AUTH_SERVER_URL}
  quarkus.oidc.client-id=cli-web-${PROJECT_ID}
  quarkus.oidc.credentials.secret=${OIDC_CLIENT_SECRET}
  quarkus.oidc.application-type=service
  quarkus.oidc.roles.source=accesstoken
  quarkus.oidc.token.auto-refresh-interval=18000

  quarkus.http.auth.permission.authenticated.paths=/api/*
  quarkus.http.auth.permission.authenticated.policy=authenticated

  # Datasource
  quarkus.datasource.db-kind=postgresql
  quarkus.datasource.username=${DB_USER:usuario}
  quarkus.datasource.password=${DB_PASSWORD:senha}
  quarkus.datasource.jdbc.url=${JDBC_URL}
  quarkus.hibernate-orm.packages=${PACKAGE_PREFIX}.${PROJECT_ID}.api.domain.model
  quarkus.hibernate-orm.dialect=${HIBERNATE_DIALECT}
  quarkus.datasource.jdbc.driver=${JDBC_DRIVER}
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
      # ${JDK_PATH}: caminho da JDK informado pelo usuário na coleta interativa
      $defaultJavaHome = '${JDK_PATH}'
      if (Test-Path $defaultJavaHome) {
          $env:JAVA_HOME = $defaultJavaHome
      } else {
          throw "JAVA_HOME não definido e o caminho do JDK '$defaultJavaHome' não existe. Configure JAVA_HOME para um JDK ${JAVA_VERSION} antes de iniciar a aplicação."
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
