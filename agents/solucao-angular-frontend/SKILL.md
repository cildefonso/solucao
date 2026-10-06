---
name: solucao-angular-frontend
description: 'Cria dinamicamente a estrutura de desenvolvimento de uma aplicação frontend Angular baseada nos padrões do SIABE-frontend. Solicita obrigatoriamente o nome do novo projeto quando não informado, parametriza identificadores Angular, diretórios, seletor, metadados, ambientes e documentação, e orienta a validação por build, testes e health check.'
argument-hint: 'Nome ou sigla do novo projeto Angular (ex.: SICLI-frontend)'
user-invocable: true
---

# Scaffold Dinâmico de Frontend Angular (Referência SIABE-frontend)

Esta skill orienta a criação de um novo projeto Angular usando o repositório `SIABE-frontend` como referência de organização, configuração e práticas de desenvolvimento. O resultado deve ser um projeto independente e parametrizado: nunca replique de forma acidental o nome, os endpoints, credenciais, textos de negócio ou configurações exclusivas do SIABE.

## Quando utilizar

Use esta skill quando o usuário solicitar criar a estrutura/esqueleto de um novo frontend Angular baseado no SIABE-frontend, ou iniciar uma aplicação Angular seguindo a estrutura corporativa de referência.

## 1. Coleta obrigatória antes de criar arquivos

Antes de criar diretórios ou arquivos, verifique os dados fornecidos pelo usuário:

1. **Nome/sigla do projeto** — obrigatório. Se ausente, pergunte: “Qual é o nome ou sigla do novo frontend? (ex.: SICLI-frontend)”. Não comece o scaffold até receber a resposta.
2. **Diretório de destino** — use o caminho que o usuário indicou; se ausente, pergunte onde criar o novo projeto. Não sobrescreva um diretório existente sem confirmação.
3. **Versão do Angular** — se não indicada, proponha a mesma major Angular observada na referência (Angular 16) e confirme se o usuário quer mantê-la ou usar outra versão. Não atualize major nem dependências silenciosamente.
4. **Integrações e configurações específicas** — pergunte, se necessárias ao projeto: URL/base da API, provedor/realm/client ID de SSO, nome exibido, versão inicial e rota de health check. Não solicite nem grave segredos reais; use variáveis/configuração externa e placeholders.

Se o nome já foi fornecido, derive os identificadores e confirme apenas dados necessários que ainda faltem. Não pergunte de novo o que já estiver claro no pedido.

## 2. Inspecione a referência antes de gerar

A referência é o projeto aberto em `SIABE-frontend`. Confirme seu estado atual antes de usá-lo; não considere documentação antiga como fonte mais confiável que a configuração ativa. Na referência analisada, o `package.json` indica Angular `^16.2`, TypeScript `~5.1`, RxJS `~7.8`, Angular Material, Keycloak, ESLint e testes Karma/Jasmine. O `README.md` menciona Angular CLI 11 e Protractor, portanto esse trecho está desatualizado e não deve ser reproduzido como fato técnico.

Use como guia, ajustando conforme a versão e necessidades confirmadas:

- `angular.json`: configurações build, serve, local/production, substituição de environments e lint.
- `package.json`/`package-lock.json`: scripts e dependências compatíveis entre si; preservar lockfile consistente.
- `src/app/app.module.ts` e `app-routing.module.ts`: composição e rotas do aplicativo. A referência usa módulos Angular e também componentes standalone; respeite a arquitetura escolhida e a versão Angular em vez de misturar padrões sem necessidade.
- `src/app/core`: infraestrutura compartilhada, autenticação/SSO, guardas, layout, header, componentes e serviços globais.
- `src/app/features`: funcionalidades de negócio, organizadas em diretórios por funcionalidade e com componentes, estilos, rotas/módulos e testes correspondentes.
- `src/app/modules`: módulos funcionais, como home/logs, quando fizerem sentido para o scaffold.
- `src/app/shared`: componentes, enumerações, modelos e serviços reutilizáveis, além do módulo shared quando aplicável.
- `src/app/models`: contratos e modelos de API/funcionalidade.
- `src/environments`: arquivos por ambiente; valores locais e de produção não devem manter endpoints/realm/client ID SIABE.
- `src/styles.scss`: estilos globais; mantenha variáveis/design tokens coerentes, sem copiar identidade visual ou conteúdo SIABE sem autorização.
- Testes `*.spec.ts`, Karma/Jasmine e configuração em `karma.conf.js`/`tsconfig.spec.json`.
- Todo componente, serviço, guard ou fluxo criado no scaffold deve vir acompanhado de testes de cobertura no respectivo `*.spec.ts`; cubra caminhos de sucesso, erro, dados ausentes, validações/limites e os lados relevantes das condições. Execute o script de cobertura disponível (na referência: `npm run test:coverage`), inspecione o resumo/LCOV por arquivo e busque 100% de cobertura de linhas e branches no código novo. Adicione testes significativos para as linhas/condições descobertas pelo relatório/Sonar; não exclua código nem reduza limiares para esconder lacunas. Se algum ramo não puder ser testado significativamente, documente o motivo.
- `tools/watch-build-restart.ps1`, Dockerfile, configuração do proxy, Nginx, Sonar e pipeline: só incluir quando fizerem sentido no destino e parametrizar portas, rotas e nomes.

A estrutura real pode evoluir. Liste/inspecione arquivos relevantes da referência no momento do uso e não invente componentes ou funcionalidades que não foram verificados.

## 3. Derivação dinâmica de nomes

Derive valores consistentes a partir do nome escolhido e use-os em todos os artefatos que realmente correspondam a identificadores do projeto:

| Conceito | Regra |
|---|---|
| Nome informado / nome exibido | `${PROJECT_NAME}` preservando a forma legível escolhida pelo usuário |
| Nome npm e id Angular | `${PROJECT_SLUG}` em minúsculas, sem espaços, com separadores válidos para npm/Angular |
| Prefixo de seletor Angular | `${SELECTOR_PREFIX}` em minúsculas e válido como prefixo de seletor |
| Título da aplicação | `${APP_TITLE}` conforme solicitado ou derivado de `${PROJECT_NAME}` |
| Diretório do projeto | Diretório de destino acordado com o usuário; não inferir o caminho a partir do slug se já foi informado |
| Versão Angular | `${ANGULAR_VERSION}` conforme escolha confirmada, compatível com TypeScript/Node e dependências |
| API/SSO | `${API_BASE_URL}`, `${SSO_URL}`, `${SSO_REALM}`, `${SSO_CLIENT_ID}` somente quando fornecidos/confirmados; caso contrário usar placeholders documentados |

Valide caracteres e nomes reservados para npm antes de criar o projeto. Não substitua cegamente todas as ocorrências de “SIABE”: referências em requisitos, conteúdo, URLs ou integrações têm significado próprio. Remova apenas marcações e valores da aplicação de referência, preenchendo-os com os dados definidos para o novo projeto.

## 4. Estrutura inicial de referência

Gere a estrutura enxuta abaixo, adaptando módulos, standalone components, lazy loading e arquivos de configuração ao Angular escolhido. Não crie diretórios vazios só para imitar a árvore:

```text
${PROJECT_SLUG}/
├── .github/
│   └── skills/ (opcional, apenas se solicitado para o novo projeto)
├── public/ (se suportado/usado pela versão escolhida)
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── auth/ (somente se SSO/autenticação fizer parte dos requisitos)
│   │   │   ├── components/ (layout, header, acesso negado, health)
│   │   │   └── services/ (serviços globais)
│   │   ├── features/
│   │   │   └── <feature>/ (componentes, HTML/SCSS, rotas e testes da feature)
│   │   ├── modules/ (módulos funcionais quando a arquitetura exigir)
│   │   ├── models/ (contratos e modelos da aplicação)
│   │   ├── shared/ (componentes, enums, modelos e serviços reutilizáveis)
│   │   ├── app-routing.module.ts (ou configuração de rotas equivalente)
│   │   ├── app.module.ts (se arquitetura baseada em NgModule)
│   │   └── app.component.*
│   ├── assets/
│   ├── environments/
│   │   ├── environment.ts
│   │   ├── environment.local.ts (se existir configuração local)
│   │   └── environment.prod.ts
│   ├── index.html
│   ├── main.ts
│   ├── polyfills.ts (quando exigido pela versão/configuração)
│   └── styles.scss
├── angular.json
├── package.json
├── package-lock.json
├── tsconfig*.json
├── karma.conf.js (quando Karma estiver selecionado)
├── proxy.conf.json (se necessário para desenvolvimento local)
├── Dockerfile / configuração Nginx (se solicitados)
└── README.md
```

A CLI Angular pode produzir arquivos e nomenclaturas diferentes por versão. Prefira `ng new`/Angular CLI compatível e depois aplique a organização necessária, em vez de gerar manualmente configuração de builder incompatível.

## 5. Regras de scaffold e parametrização

- Inicialize `package.json`, projeto em `angular.json`, nome npm e prefixo de seletor com os valores derivados.
- Mantenha nomes e caminhos alinhados em imports, referências de build, rotas, testes e scripts. Não altere caminhos de ambiente sem atualizar `fileReplacements` do `angular.json`.
- Separe responsabilidades: `core` para infraestrutura singleton/global, `features` para domínio, `shared` para elementos reutilizados e `models` para contratos. Não coloque regra de negócio em componentes genéricos.
- Defina rotas principais e uma rota de health (`/health`) apenas se requerida; qualquer endpoint de health deve ser simples, previsível e coberto por teste. Não confunda health do frontend estático com health da API.
- Se o usuário solicitar autenticação, configure Keycloak ou o provedor confirmado por abstração/configuração de ambiente. Não copie o client ID `cli-web-abe`, realm/URLs do SIABE, nem segredos. Use callback/SSO apropriado e guarde segredos fora do bundle frontend.
- Ambientes devem declarar apenas configurações públicas necessárias à aplicação, com valores de exemplo não secretos. Não embuta credenciais privadas em aplicações browser-side.
- Configure `proxy.conf.json` somente para desenvolvimento e com o host de destino confirmado. Não propague logs verbosos ou `secure: false` para produção.
- Inclua testes de componentes, serviços, guards e rotas conforme criados. Siga o runner e framework que o Angular/CLI do projeto suporta; não mantenha referências antigas a Protractor se não estiver configurado.
- Em arquivos TypeScript e `*.spec.ts`, siga rigorosamente a regra ESLint `padding-line-between-statements` da configuração do projeto: mantenha declarações `const`/`let`/`var` consecutivas sem linhas vazias entre elas e insira uma linha em branco entre o bloco de declarações e a primeira instrução executável. Insira também uma linha em branco antes de cada `return`. Ao escrever testes, aplique a separação também entre preparação baseada em declarações e a próxima instrução (por exemplo, configuração de mocks/variáveis e chamada do componente); não deixe esses casos para o lint/Sonar encontrar depois.
- Inclua ESLint, Material, Keycloak, Docker, Nginx, Sonar ou scripts PowerShell somente quando necessários e confirme compatibilidade/versionamento. Evite instalar dependências não pedidas.
- O README deve documentar versão efetivamente criada, instalação, comandos, ambientes, proxy, testes e execução; não copiar instruções desatualizadas da referência.
- Se criar script local de build/restart, mantenha-o no contexto do projeto e evite watchers infinitos durante validação automatizada.

## 6. Validação obrigatória

Após criar o scaffold:

1. Verifique os arquivos gerados, nomes derivados, caminhos, configurações de ambiente, rotas e ausência de valores específicos do SIABE que não tenham sido aprovados.
2. Instale dependências de forma compatível com o lockfile e execute build de produção, lint e testes disponíveis no `package.json`. O lint deve terminar sem erros — em particular, sem ocorrências de `padding-line-between-statements` — antes de considerar a validação concluída.
3. Execute também o script de cobertura disponível (na referência: `npm run test:coverage`), inspecione a cobertura dos arquivos criados e confirme que o relatório LCOV foi gerado no caminho consumido pelo Sonar, quando configurado. Resolva lacunas em linhas/branches do código novo com testes antes de concluir.
4. Corrija falhas introduzidas pelo scaffold; não oculte erros existentes nem trate `get_errors`/diagnósticos do editor como substituto da execução do lint ou da cobertura. Se uma ferramenta não puder executar por dependência ausente, resolva a instalação compatível com o lockfile ou informe explicitamente o bloqueio; registre testes que não puderam executar e o motivo.
5. Inicie/reinicie a aplicação usando o script adequado. Valide a página/rota de health definida para o frontend e, quando aplicável, o endpoint de API afetado; informe se a checagem da API depende de serviço externo.
6. Finalize informando diretório, nome/prefixo, versão Angular, arquitetura criada, comandos executados e qualquer configuração ainda pendente.

## 7. Critério de conclusão

A estrutura só está concluída quando o projeto é dinâmico em nome/id/prefixo e configurações fornecidas, compila com a versão escolhida, tem instruções atualizadas e não contém configurações específicas SIABE copiadas por engano. Se faltar nome ou destino, interrompa e pergunte antes de criar arquivos.
