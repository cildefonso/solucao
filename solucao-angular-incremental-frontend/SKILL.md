---
name: solucao-angular-incremental-frontend
description: 'Implementa uma funcionalidade incremental em uma aplicação Angular existente: lê especificações e arquitetura real, solicita o path do backend para integrações com APIs, confirma o contrato e entrega componente, serviço, modelos, rotas, navegação, traduções e testes. Use para adicionar funcionalidade, tela, fluxo ou consulta ao SIABE-frontend ou a outro frontend Angular existente.'
argument-hint: 'Descreva a funcionalidade e critérios de aceite; para integrações com API, informe o path do projeto backend ou da classe resource/controller'
user-invocable: true
---

# Implementação Incremental de Funcionalidade Angular

Esta skill implementa uma funcionalidade completa em um frontend Angular já existente. Usa a feature `demonstrativo-mensal` do SIABE-frontend como exemplo de organização e fluxo, mas a fonte de verdade é sempre o código e as especificações atuais do projeto-alvo. Não cria um novo workspace e não replica regras de negócio do demonstrativo quando não forem aplicáveis.

## Quando utilizar

Use ao adicionar uma tela, consulta, fluxo de usuário, formulário, integração frontend/API ou outra funcionalidade a um projeto Angular existente. Antes de editar, leia as especificações do usuário e os documentos de requisitos disponíveis no repositório.

## 1. Descoberta e especificação — antes de editar

1. Confirme o workspace Angular correto. Inspecione `package.json`, `angular.json`, rotas, módulo raiz, estrutura de `src/app`, feature semelhante mais próxima, serviços/modelos usados, ambiente, configuração de testes e navegação.
2. Determine se a funcionalidade consome ou altera APIs. Se sim, obtenha obrigatoriamente do usuário o path absoluto do projeto backend ou da classe `Resource`/`Controller` relevante antes de implementar a integração. Se o path não foi informado, pergunte por ele antes de codificar; use como exemplo de formato `C:\caixa\desenv\backend\java\legado\SIABE-micro\src\main\java\br\gov\caixa\siabe\api\resource\BeneficioContaResource.java`. Esse caminho é apenas exemplo: nunca o trate como path do projeto atual sem confirmação. Para funcionalidades sem integração com API, não solicite path do backend.
3. Inspecione o código backend indicado como fonte de verdade do contrato: resource/controller e, quando necessário, serviços/use cases, DTOs/models, testes e especificação OpenAPI. Identifique rota, método HTTP, parâmetros/body, formatos de sucesso/erro, autenticação e regras relevantes. Se o path não existir ou não estiver acessível, peça ao usuário um path válido ou o contrato OpenAPI equivalente; não invente contrato.
4. Procure especificações fornecidas no pedido e artefatos existentes relevantes (por exemplo, `README.md`, documentação de funcionalidade, histórias, critérios de aceite, OpenAPI ou contratos de API). Leia os arquivos relevantes integralmente antes de propor comportamento.
5. Extraia requisitos existentes e identifique o que está definido e o que falta:
   - objetivo da funcionalidade, usuário/permissão e caminho de navegação;
   - campos, formatos, validação e regras de negócio;
   - ações disponíveis e resultado esperado;
   - endpoint, método HTTP, parâmetros/body, envelope e tipos de sucesso/erro;
   - estados loading, vazio, sucesso, validação e falha;
   - acessibilidade, responsividade, idioma e critérios de aceite.
6. Se faltarem dados que mudem comportamento, integração, acesso ou critério de aceite, pergunte ao usuário antes de codificar. Agrupe perguntas objetivas em uma única interação, se possível. Não invente endpoint, payload, regra de negócio, perfil de acesso nem comportamento para lacunas importantes. Se a ferramenta de perguntas estiver disponível, use-a; caso contrário, pergunte diretamente no chat.
7. Se a especificação estiver suficiente, resuma brevemente o comportamento e o escopo a implementar e prossiga. Mantenha explícitas as suposições não críticas; não interrompa por preferências visuais menores quando o design system existente definir o padrão.

## 2. Padrões observados no SIABE-frontend

A referência possui Angular 16 e TypeScript 5.1; a feature `demonstrativo-mensal` exemplifica estes elementos:

- `src/app/features/demonstrativo-mensal/`: página Angular com TypeScript, template HTML, SCSS e teste `*.spec.ts`.
- Componente standalone com `ChangeDetectionStrategy.OnPush`, `inject()`, Reactive Forms e signals para estado/derivações. Use esse padrão se compatível com a versão instalada e com a convenção ativa; não converta o projeto inteiro nem misture padrões sem necessidade.
- `src/app/shared/services/demonstrativo-mensal.service.ts`: chamada tipada via `HttpClient`, `HttpParams`, `Observable` e endpoint derivado de `environment.endpoint`.
- `src/app/models/demonstrativo-mensal.model.ts` e `api-response.model.ts`: modelos tipados para filtros, resposta e erro.
- Rota protegida e componente conectado ao `ContentLayoutComponent` em `src/app/app-routing.module.ts`; existe também um routing module da feature. Verifique qual registro é efetivamente usado antes de escolher uma única estratégia e evite registrar rotas duplicadas.
- `src/app/core/components/header/header.component.*` e `TranslationService`: links de menu e dicionário tipado com textos pt/en/es. Altere navegação e traduções apenas se o requisito incluir acesso pelo menu/interface multilíngue; quando adicionar strings ao dicionário existente, atualize o tipo e todos os idiomas.
- Testes Karma/Jasmine em arquivos `*.spec.ts`, com dependências providas via `TestBed` e serviços simulados com spies/Observable. Amplie o padrão local para cobrir critérios e estados da funcionalidade nova.
- `src/styles.scss` contém variáveis globais de tema e espaçamento. Prefira estilos locais na feature e tokens existentes; evite redefinir globalmente estilos de outras páginas.

Esses são achados da referência, não regras universais. Confirme arquivos, padrões, versões e roteamento reais no momento da execução; siga o projeto aberto e as especificações atuais. Não assuma que funcionalidades/configurações mencionadas em documentos estão implementadas até conferi-las no código.

## 3. Desenho da mudança

Antes de editar, trace a feature de ponta a ponta e determine os arquivos necessários. Para um fluxo típico de consulta, considere, somente quando exigidos:

- pasta `src/app/features/<feature>/`: componente/página, HTML, SCSS e specs;
- `src/app/models/`: interfaces/tipos de request, response e erro;
- `src/app/shared/services/` ou o diretório de serviços definido pelo projeto: serviço HTTP dedicado;
- rota da aplicação/feature com layout e guard apropriados;
- navegação/menu e traduções, se a funcionalidade precisar ser descoberta por esses pontos;
- módulos, providers, imports, ambientes ou configuração de proxy somente se a implementação realmente os exigir;
- documentação existente, quando especificações/uso forem parte da convenção do repositório.

Mantenha a mudança localizada e integrada. Não altere serviços, estilos, rotas ou padrões sem relação com o requisito. Não faça refatorações oportunistas nem adicione dependências sem necessidade demonstrada. Se o workspace já tiver alterações não relacionadas, preserve-as e limite a edição aos arquivos necessários.

## 4. Implementação da feature

### Interface e estado

- Construa uma página coesa na pasta da feature, separando lógica TypeScript, template e SCSS conforme o padrão existente.
- Use Reactive Forms para formulários com validações/regras e mostre erros junto aos campos, associados semanticamente; marque os campos como tocados no submit inválido.
- Represente carregamento, resultado, ausência de dados e falha de forma distinta e acessível (`role="status"`/`role="alert"` quando pertinente). Desabilite ações incompatíveis durante carregamento e ofereça limpar/cancelar apenas se previsto.
- Mantenha cálculo/regra de negócio fora do template quando ficar complexo. Trate dados da API com tipos explícitos, sem `any` injustificado.
- Preserve responsividade, semântica HTML, navegação por teclado e componentes/tokens visuais existentes. Não copie identidade ou texto específico do demonstrativo sem requisito.

### Serviço e contrato

- Centralize comunicação HTTP num serviço Angular; injete dependências conforme convenção atual. Construa URLs com a configuração de ambiente já usada pelo projeto, nunca espalhe base URL pela UI.
- Implemente exatamente o contrato confirmado: método, rota, query params/body, tipos, envelope, transformação e tratamento de erros. Não presuma envelope `ApiResponse<T>` para APIs que não o utilizam.
- Normalize apenas valores definidos pela especificação. Não envie parâmetros artificiais vazios nem converta formatos sem validar o contrato.
- Respeite interceptors, autenticação e tratamento global existentes; não duplique lógica de token ou logs.

### Rota, permissão e descoberta

- Registre a rota uma única vez, seguindo a convenção efetivamente utilizada. Reaproveite layout/guard de autenticação e verificação de perfil/roles existente quando exigidos.
- Não deixe a página protegida apenas por esconder o link do menu. Restrições de autorização devem seguir os guards/roles da aplicação.
- Adicione item de menu, breadcrumb, página inicial ou traduções apenas conforme os critérios de aceite. Garanta que destinos e URLs não colidam com rotas existentes.

## 5. Testes obrigatórios

Crie ou amplie specs para validar comportamento observável, incluindo, conforme a feature:

- inicialização e valores/validadores dos formulários;
- submissão inválida sem chamada HTTP e submissão válida com parâmetros/body corretos;
- sucesso com dados e resposta sem dados;
- erro de API, mensagem exibida e encerramento do estado de carregamento;
- ação de limpar/reiniciar, regras de habilitar/desabilitar e cálculos relevantes;
- apresentação e roteamento/permissão quando forem parte do comportamento;
- navegação, strings e acesso semântico essenciais no template.

Simule o serviço HTTP para testes do componente. Para o serviço, use `HttpTestingController` se isso estiver alinhado ao setup presente. Evite depender de API real, SSO ou rede nos testes unitários. Teste critérios de aceite, não implementação interna frágil.

**Cobertura obrigatória da funcionalidade:** junto com cada funcionalidade, crie/atualize os `*.spec.ts` para cobrir o código novo e alterado, não apenas o caminho feliz. Inclua cenários para resultados, erros, dados ausentes, limites/validações e os dois lados das decisões condicionais relevantes. Depois execute o script de cobertura do projeto (na referência: `npm run test:coverage`) e examine o relatório LCOV/resumo por arquivo. Busque 100% de cobertura de linhas e branches no código novo/alterado; acrescente testes significativos para toda linha/condição descoberta pelo relatório/Sonar. Não exclua código da análise nem reduza o limiar para ocultar falta de cobertura. Se algum caminho não puder ser exercitado de forma significativa, registre qual e por quê.

**Formatação ESLint obrigatória:** siga a regra `padding-line-between-statements` configurada no projeto em todo código TypeScript, incluindo componentes, serviços e `*.spec.ts`. Mantenha declarações `const`/`let`/`var` consecutivas sem linhas vazias entre elas; coloque uma linha em branco entre o bloco de declarações e a primeira instrução executável; e sempre deixe uma linha em branco antes de `return`. Nos testes, separe explicitamente o bloco de preparação (mocks e dados) da primeira ação executada, para que o lint não aponte `Expected blank line before this statement`.

## 6. Validação e ciclo local

Após editar código, valide conforme o `package.json` e a configuração do projeto:

1. Execute o build de produção e lint disponível (na referência: `npm run build` e `npm run lint`). O lint precisa terminar sem erros, especialmente sem violações de `padding-line-between-statements`; não deixe esses avisos para o Sonar ou para o pipeline.
2. Execute testes não interativos, usando script apropriado (na referência: `npm run test:ci`, configurado para Firefox headless). Inspecione resultados e corrija falhas introduzidas pela alteração sem mascarar falhas preexistentes.
3. Execute também o script de cobertura disponível (na referência: `npm run test:coverage`) e inspecione a cobertura do componente/serviço da feature, incluindo branches. Feche as lacunas de cobertura do código novo/alterado com testes antes de concluir; confirme que o relatório LCOV foi gerado no caminho consumido pelo Sonar, quando configurado.
4. Inicie ou reinicie a aplicação no modo local usando o comando existente (na referência: `npm run start-local`, que usa `environment.local.ts`). Evite iniciar outra instância se uma já estiver ativa; não encerre processos alheios sem autorização.
5. Valide o endpoint/rota afetado no navegador e o health check da aplicação quando disponível (a referência oferece rota `/health`). Se a funcionalidade depender de backend ou SSO externo, identifique separadamente o que foi validado e o que está bloqueado por indisponibilidade/configuração externa.
6. Se houver falha de build/teste/cobertura/startup, investigue e corrija as falhas relacionadas à mudança. Não declare validação concluída sem evidência dos comandos/checagens executados. Se um comando não puder rodar por falta de browser, serviço, credencial ou ambiente, informe a limitação objetivamente.

## 7. Entrega

Ao terminar, informe de forma concisa:

- funcionalidade e fluxos implementados;
- arquivos/áreas principais alterados;
- rotas, endpoint/contrato e permissões adicionados, se aplicável;
- testes, build, lint, startup e health check efetivamente validados;
- pendências, suposições ou integrações externas não verificadas.

Considere a funcionalidade concluída apenas quando os requisitos confirmados estão implementados verticalmente (UI, validação, integração, navegação/acesso e testes pertinentes) e a validação local foi realizada ou suas limitações foram registradas.
