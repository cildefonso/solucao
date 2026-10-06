# Solução 
<small>by solucao</small>

**Turn legacy systems into executable specifications for AI agents.**

> 📄 **Paper:** [Solicao: A Reverse Documentation Engineering Framework for Converting Legacy Software into Operational Specifications for AI Agents](https://arxiv.org/abs/2605.18684) — Macedo & da Costa, May 2026.

[![Solucao paper](solucao-paper.png)](https://arxiv.org/abs/2605.18684)

[![English Docs](https://img.shields.io/badge/DOCS-English-009c3b?style=for-the-badge&logo=material-for-mkdocs&logoColor=white&labelColor=2d2d2d)](https://cildefonso.github.io/solucao/)<br>
[![Português Docs](https://img.shields.io/badge/DOCS-Portugu%C3%AAs-ffcc00?style=for-the-badge&logo=material-for-mkdocs&logoColor=black&labelColor=2d2d2d)](https://cildefonso.github.io/solucao/pt/)<br>
[![Español Docs](https://img.shields.io/badge/DOCS-Espa%C3%B1ol-c60b1e?style=for-the-badge&logo=material-for-mkdocs&logoColor=white&labelColor=2d2d2d)](https://sandeco.github.io/solucao/es/)

A Solução é um framework de engenharia solucao de especificações. Ao instalá-lo em um projeto legado, ele coordena uma equipe de agentes de IA especializados para analisar o código existente e gerar especificações completas e rastreáveis, prontas para uso por qualquer agente de programação.

---

![Solucao installer](solucao-installer.png)

---

## Porque a Solução existe?

A maioria dos sistemas em produção carrega anos de conhecimento acumulado: regras de negócio implícitas, decisões arquiteturais não documentadas e lógica crítica oculta em códigos que ninguém deseja modificar. Esse conhecimento existe, mas encontra-se aprisionado.

Os agentes de IA são transformadores na criação e na evolução de software, porém dependem de especificações para operar com segurança. Em sistemas novos, escreve-se a especificação e o agente a executa. Em sistemas legados — ou naqueles construídos exclusivamente com vibe coding — não há especificação: o agente não tem como saber o que não pode quebrar.

**A Solução é a ponte entre o sistema legado e os agentes de IA.**

Ele analisa o código existente, extrai o conhecimento acumulado (regras de negócio, fluxos, contratos entre módulos e decisões arquiteturais retroativas) e transforma tudo em especificações executáveis e rastreáveis, prontas para qualquer agente de codificação.

O resultado não é uma documentação destinada à leitura humana. Trata-se de **contratos operacionais** que permitem a um agente evoluir o sistema com fidelidade ao que já existe.

---

## Instalação

Na raiz do projeto legado:

```bash
npx solucao install
```

O instalador irá:
1. Detectar os motores de IA presentes no ambiente (Claude Code, Codex, Cursor etc.)
2. Perguntar quais agentes devem ser instalados — todos vêm selecionados por padrão
3. Coletar o nome do projeto, o idioma e as preferências
4. Copiar os agentes para `.agents/skills/` (e para `.claude/skills/`, no caso do Claude Code)
5. Criar o arquivo de entrada do motor (`CLAUDE.md`, `AGENTS.md` etc.)
6. Criar a estrutura `.solucao/` com o estado, a configuração e o plano
7. Gerar um manifesto SHA-256 para atualizações seguras

> Solução **nunca exclui nem modifica** os arquivos existentes em seu projeto.
> Os agentes gravam apenas em `.solucao/` e na pasta de saída (`_solucao_sdd/`, por padrão).

**Requisitos:** Node.js 18+

---

> [!IMPORTANTE]
> ### 🔒 Imutabilidade garantida do projeto legado
>
> O instalador apenas cria novos arquivos (`CLAUDE.md`, `AGENTS.md`, `.agents/skills/` etc.) e **nunca modifica nem exclui nenhum arquivo existente** em seu projeto. Durante a análise, os agentes operam sob uma diretriz rigorosa e inviolável: **todas as gravações restringem-se a `.solucao/` e `_solucao_sdd/`** — nenhum outro arquivo de seu projeto é alterado.

> > [!CUIDADO]
> ### 💾 Faça um backup do seu projeto antes de começar
>
> Embora o Solução nunca modifique seus arquivos, os agentes de IA podem cometer erros. **Recomendamos enfaticamente:**
>
> 1. **Versionar o projeto no Git** — certifique-se de que todos os arquivos estejam commitados antes de iniciar a análise
> 2. **Manter o repositório no GitHub** (ou GitLab, Bitbucket) — para dispor de uma cópia remota segura
> 3. **Fazer uma cópia local da pasta** — um simples `cp -r meu-projeto meu-projeto-backup` protege contra qualquer imprevisto
>
> Caso ocorra algum imprevisto durante a análise, é possível restaurar o estado original com `git restore .` ou a partir da cópia de backup.

> [!AVISO]
> 🔑 **SOlução não solicita, armazena ou transmite chaves de API de qualquer serviço LLM.** Toda a inteligência é delegada ao agente de IA já presente em seu ambiente (Claude Code, Codex, Cursor etc.), sem dependências externas de autenticação.

---

## Como usar

Após a instalação, abra o projeto no agente AI e ative a Solução:

```
/solucao
```

Para motores sem suporte a slash commands (como o Codex):

```
solucao
```

O solucao se apresentará, criará um plano de exploração personalizado e coordenará toda a análise. O progresso é salvo em `.solucao/state.json` a cada checkpoint — caso a sessão seja interrompida, basta digitar `solucao` para retomar de onde parou.

For other workflows, use the matching entry command:

| Meta | Comando |
|------|---------|
| Analisar um sistema legado existente e produzir especificações | `/solucao` |
| Executar a mesma análise de ponta a ponta, sem paradas intermediárias | `/solucao-autonoma` |
| Iniciar um projeto totalmente novo a partir de uma ideia descrita em uma única linha | `/solucao-novo` (acrescente `expresso` para avançar até o código) |
| Evoluir o sistema uma funcionalidade por vez, da especificação ao código | `/solucao-enviar` |
| Acrescentar um breve complemento à funcionalidade recém-entregue | `/solucao-add` |
| Reintegrar à extração uma funcionalidade já entregue | `/solucao-sincronizar` |
| Reconstruir o sistema legado em uma stack moderna | `/solucao-migrar` |
| Gerar um minissite em HTML com o conhecimento extraído | `/solucao-documentos` |
| Rastrear e corrigir defeitos com rastreabilidade causal | `/solucao-depuracao`, `/solucao-depuracao-resolver` |
| Estimar esforço e preço com base nas especificações | `/solucao-perfil-precificacao`, `/solucao-fins-precificacao`, `/solucao-estimativa-preco` |

Cada orquestrador faz uma pausa entre os agentes e solicita `CONTINUAR` antes de prosseguir, de modo que você mantém o controle de cada etapa.

### Execuções autônomas

Dois comandos concentram todas as perguntas em uma **única entrevista no início** e, em seguida, são executados sem interrupções, para sessões em que ninguém está acompanhando o terminal (modo YOLO do Claude Code ou equivalente):

- `/solucao-autonoma` — o pipeline completo de Discovery, com os mesmos agentes e os mesmos checkpoints do `/solucao`.
- `/solucao-novo expresso "<sua ideia>"` — projeto greenfield, da ideia até o código implementado, encadeando o ciclo de evolução após as especificações.

Ambos preservam integralmente a regra não destrutiva: as gravações permanecem restritas a `.solucao/` e às pastas de saída, e nenhum comando destrutivo ou com efeitos externos (exclusão, `git push`, publicação, instalação) é executado por conta própria. As dúvidas que surgirem ao longo do processo são registradas com o selo 🟡, em vez de interromperem o fluxo.

---

## Como funciona

O pipeline de Discovery (`/solucao`) é o núcleo do framework: uma sequência de 5 fases orquestrada pelo agente **Solucao**.

```
Reconhecimento  Escavação       Interpretação   Geração         Revisão
  Explorador    Arqueólogo        Detetive      Redator         Revisor
                                  Arquiteto
```

Agentes independentes (executáveis em qualquer fase): **Visor**, **Mestre de Dados**, **Design System**, **Extrator de Essência**, **Reconstrutor**.

Uma vez existentes as especificações, é possível avançar em três direções, conforme o objetivo:

```
Descoberta (/solucao)
        │
        ├── /solucao-enviar    Evoluir o sistema, das especificações ao código
        ├── /solucao-migrar    Reconstruir o sistema legado em uma stack moderna
        └── /solucao-documentos       Gerar um minissite em HTML a partir das especificações
```

Para um projeto **greenfield** (sem sistema legado a ser extraído), comece pelo `/solucao-novo`. Ele conduz o processo desde uma ideia descrita em uma única linha até as especificações SDD e, em seguida, transfere a continuidade para o `/solucao-enviar`.

---

## Agents

A Solução organiza seus agentes em **dez equipes especializadas**. A equipe Discovery (núcleo de agentes da Solução) e os agentes de bugs vêm sempre instalados; sete equipes já vêm selecionadas no instalador, enquanto a instalação das equipes de tradução é opcional.

| Equipe | Finalidade | Comando de entrada |
|--------|------------|--------------------|
| **Núcleo de Agentes do Solução** (Discovery) | Analisar o sistema legado existente e produzir especificações | `/solucao` |
| **Agentes de Ideação** | Refinar uma ideia inicial antes que exista qualquer artefato de desenvolvimento, tanto em projetos greenfield quanto em sistemas legados | `/solucao-brainstorm` |
| **Agentes de Novo Projeto** | Iniciar um novo projeto (greenfield) a partir de uma ideia descrita em uma única linha e produzir especificações | `/solucao-novo` |
| **Agentes de Evolução de Código** | Evoluir o sistema das especificações ao código em execução, uma funcionalidade por vez | `/solucao-enviar` |
| **Agentes de Migração** | Converter as especificações do sistema legado em um plano de reconstrução para uma stack moderna | `/solucao-migrar` |
| **Agentes de Precificação e Dimensionamento** | Estimar esforço, dimensão e preço com base nas especificações | `/solucao-pricing-*` |
| **Equipe de Documentação** | Gerar um minissite em HTML autocontido com o conhecimento extraído | `/solucao-documentos` |
| **Agentes de Defeitos** | Rastrear, discutir e corrigir defeitos com rastreabilidade causal até as especificações | `/solucao-depuracao` |
| **Agentes de Qualidade de Código** | Aprimorar o código existente sem alterar seu comportamento: refatorar, otimizar, padronizar e remover código morto | `/solucao-refactor` |

### Equipe de Descoberta, obrigatório

Estes agentes executam o pipeline principal do `/solucao`.

| Agente | Função |
|--------|--------|
| **Solucao** | Orquestrador central. Coordena todos os agentes, salva os checkpoints e orienta o usuário |
| **Explorador** | Mapeia a superfície: estrutura de pastas, linguagens, frameworks, dependências e pontos de entrada |
| **Arqueólogo** | Análise aprofundada, módulo por módulo: algoritmos, fluxos de controle e estruturas de dados |
| **Detetive** | Extrai o conhecimento de negócio implícito: regras, ADRs retroativos, máquinas de estado e permissões |
| **Arquiteto** | Sintetiza tudo em diagramas C4, DER completo, mapa de integrações e dívida técnica |
| **Redator** | Gera especificações na forma de contratos operacionais com rastreabilidade até o código |

### Equipe de Discovery, opcional (instalada por padrão)

| Agente | Função |
|--------|--------|
| **Revisor** | Revisa as especificações, identifica inconsistências e valida as lacunas com o usuário |
| **Visor** | Documenta a interface a partir de capturas de tela, sem que o sistema precise estar em execução |
| **Mestre de Dados** | Análise completa do banco de dados: DDL, migrations, ORM, DER, triggers e procedures |
| **Design System** | Extrai os design tokens: cores, tipografia, espaçamento, temas e componentes |
| **Extrator de Essência** | Produz uma única especificação executiva (`soul.md`) com o propósito, as entidades centrais e as decisões fundadoras do sistema; útil logo após o Explorador |
| **Ajuda dos Agentes** | Explica cada agente do Solução por meio de analogias; útil para iniciantes |
| **Reconstrutor** | Gera um plano de reconstrução bottom-up a partir das especificações e implementa uma tarefa por vez, economizando tokens. Ativação: `/solucao-reconstrutor` |
| **Autônomo** | Executa a mesma sequência do `/solucao` de ponta a ponta, com uma única entrevista no início e sem paradas intermediárias. Ativação: `/solucao-autonoma` |

### Agentes de Ideação (antes de qualquer construção)

Destinados ao momento em que a ideia ainda está em estado bruto. Funcionam em **ambos** os cenários: projetos greenfield e evolução de um sistema legado existente. Ative com `/solucao-brainstorm`, e o orquestrador conduzirá o pipeline `Enquadrador → Prospector → Desafiador → Árbitro → Pré-Especificação`, com um checkpoint `CONTINUAR` entre os agentes. Nenhuma etapa desta equipe produz código.

Os artefatos ficam em uma pasta por sessão: `_solucao_sdd/brainstorms/<NNN>-<nome-curto>/`. A sessão ativa é registrada em `.solucao/active-ideation.json`. A transferência final é feita para o `/solucao-novo` em projetos greenfield, para o `/solucao-requisitos` em sistemas legados ou para o `/solucao-migrar` quando a intenção for uma reconstrução.

| Agente | Função |
|--------|--------|
| **Solução Brainstorm** | Orquestrador. Identifica se o cenário é greenfield ou legado, abre a pasta da sessão e direciona o fluxo conforme a etapa física. Não grava, por si só, nenhum artefato do pipeline |
| **Enquadrador** | Separa o problema da solução e não permite que uma solução se passe por problema. Produz `framing.md` com o job to be done e o custo de não fazer nada |
| **Prospector** | Abre de 3 a 5 caminhos substancialmente distintos, incluindo sempre "não construir" e "usar uma solução pronta". Não está autorizado a fazer recomendações. Produz `options.md` |
| **Desafiador** | Premortem, a premissa capaz de inviabilizar cada opção, o teste de baixo custo para verificá-la e o custo oculto no sistema legado. Adversarial por concepção. Produz `risks.md` |
| **Árbitro** | Pontua as opções em relação aos riscos e recomenda uma delas com um trade-off explícito. A escolha permanece humana, e qualquer divergência em relação à recomendação é registrada como tal. Produz `decision.md` |
| **Pré-Especificação** | Converte a decisão no pacote mínimo de que o próximo pipeline necessita: escopo mínimo, não objetivos, critério de conclusão e marcadores `[DOUBT]` em aberto. Não redige requisitos nem arquitetura. Produz `pre-spec.md` |

### Agentes de Novo Projeto (greenfield)

Destinados a projetos que ainda não existem. Ative com `/solucao-novo`, e o orquestrador conduzirá o pipeline `Idealizador → Pesquisador → Projetista → Especificação SDD`, com um checkpoint `CONTINUAR` entre os agentes. Ao final, a transferência sugere o `/solucao-enviar` para levar as especificações ao código.

O orquestrador possui **dois modos**. No modo *guiado* (padrão), ele faz uma pausa a cada agente e encerra o processo nas especificações. No modo *expresso* (`/solucao-novo expresso "<sua ideia>"`), todas as perguntas são concentradas em uma única entrevista no início e, após o comando `INICIAR`, o pipeline é executado sem interrupções, passando pelas especificações e seguindo para o ciclo de evolução (`requisitos → plano → pendencia → codificacao`) até que o código esteja gravado em disco.

| Agente | Função |
|--------|--------|
| **Solução Novo** | Orquestrador. Lê o briefing inicial, percorre o pipeline e salva `newproject_progress` em `state.json` |
| **Idealizador** | Brainstorm estruturado com 6 perguntas divergentes (problema raiz, valor, alternativas, público, métricas de sucesso e premissas perigosas). Produz `_solucao_sdd/ideation.md` |
| **Pesquisador** | Transforma a descrição inicial do público em 1 a 3 personas estruturadas, com suas respectivas jornadas. Produz `_solucao_sdd/personas.md` |
| **Projetista** | Sintetiza a ideação e as personas em um PRD completo (problema, métricas, escopo, não objetivos, restrições e riscos). Produz `_solucao_sdd/prd.md` |
| **Especificação SDD** | Decompõe o PRD em componentes lógicos e redige uma especificação SDD por componente, com pontuação de qualidade automática. Incorporada a partir da skill global `sdd-spec`. Produz `_solucao_sdd/sdd/*.md` |

### Agentes de Evolução de Código (evolução)

A ponte entre as especificações e o código em execução. Pipeline: `requisitos → clarificar → quality → plano → pendencia → auditoria → codificacao → sincronizar`. Utilize o `/solucao-enviar` como ponto de entrada: ele identifica a **etapa física** da funcionalidade ativa (inspecionando os artefatos em disco, e não os metadados) e sugere o próximo agente.

| Agente | Função |
|--------|--------|
| **Solução Evolução** | Orquestrador. Identifica a etapa física e sugere a próxima skill. Nunca executa código diretamente |
| **Requisitos** | Transforma uma ideia descrita livremente em `requisitos.md`, ancorado no sistema legado, com marcadores `[DOUBT]`, lacunas e glossário |
| **Clarificar** | Até 5 perguntas direcionadas para resolver os marcadores `[DOUBT]` no próprio documento |
| **Qualidade** | Auditor somente leitura da clareza da redação. Produz `requisitos-auditoria.md` |
| **Plano** | Traduz os requisitos em uma proposta técnica expressa como um **delta em relação ao sistema legado**. Produz `roadmap.md`, `investigation.md`, `data-delta.md`, `onboarding.md` e `interfaces/` |
| **Pendência** | Decompõe o roadmap em ações atômicas distribuídas em cinco fases, com IDs estáveis, dependências e marcadores de paralelismo. Produz `actions.md` |
| **Auditoria** | Verificação cruzada, somente leitura, entre requisitos, roadmap e ações. Produz `auditoria/cross-check.md` |
| **Codificação** | Executa o `actions.md`, marca as caixas de seleção e grava `progress.jsonl`, `legacy-impact.md` e `regression-watch.md` |
| **Adição** | Opcional e repetível após a codificação. Aplica uma breve emenda à funcionalidade entregue: registra-a na seção `## Emendas` do `requisitos.md` e, em seguida, a implementa. Recusa qualquer alteração que exija nova dependência, mudança de schema ou de contrato, nova superfície pública, novo fluxo de autenticação ou qualquer item fora do escopo da funcionalidade ativa. Ativação: `/solucao-add` |
| **Sincronização** | Etapa opcional de convergência após a codificação. Condensa a funcionalidade entregue em um adendo em `_solucao_sdd/addenda/`, de modo que a extração continue descrevendo o sistema como ele é atualmente até a próxima reextração completa. Nunca edita os artefatos originais. Ativação: `/solucao-sincronizar` |
| **Princípios** | Gerencia as regras permanentes do projeto (`principios.md`) e emite relatórios de impacto quando elas são alteradas |
| **Retomada** | Substitui a funcionalidade ativa por outra da fila `paused-features` |

### Equipe de Migração

Utilize após o `/solucao` quando o objetivo for reconstruir o sistema legado em uma stack moderna. Ative com `/solucao-migrar`. Pipeline: `Consultor de Paradigma → Curador → Estrategista → Designer → Tradutor de Telas → Inspetor`, com uma pausa para revisão humana entre os agentes. Todos os artefatos são gravados em `_solucao_sdd/migration/`.

| Agente | Função |
|--------|--------|
| **Consultor de Paradigma** | Identifica o paradigma do sistema legado, infere o paradigma de destino e exige uma decisão consciente do usuário |
| **Curador** | Decide, regra por regra: MIGRAR, DESCARTAR ou DECISÃO HUMANA |
| **Estrategista** | Avalia as estratégias Strangler Fig, Big Bang, Parallel Run e Branch by Abstraction e recomenda uma delas |
| **Designer** | Elabora a arquitetura de destino, o modelo de domínio, o modelo de dados e o plano de migração de dados |
| **Tradutor de Telas** | Converte as telas do sistema legado em especificações executáveis em 2 fases (definição do modo e geração das especificações), emitindo golden files para o Inspetor quando há um oráculo disponível |
| **Inspetor** | Define como comprovar que o novo sistema é comportamentalmente equivalente ao legado, por meio de especificações de paridade em Gherkin |

### Equipe de Precificação e Dimensionamento

Três agentes que atuam sobre as especificações para estimar esforço, dimensão e preço. Ative com `/solucao-perfil-precificacao`, `/solucao-fins-precificacao` e `/solucao-estimativa-preco`.

### Tradutores (adaptadores de entrada)

Utilize quando o "código" do sistema legado não for código-fonte, mas sim um artefato estruturado, como um workflow visual. Gera a especificação SDD e prepara o estado para que o pipeline principal assuma a continuidade.

| Agente | Função |
|--------|--------|
| **Tradutor N8N** | Lê workflows do N8N exportados em JSON e produz especificações SDD prontas para reimplementação em Python. Ativação: `/solucao-n8n` |

### Equipe de Documentação (minissite em HTML)

Após a conclusão do Discovery, esta equipe transforma o conhecimento extraído em um minissite em HTML autocontido, gravado em `_solucao_documentos/`. Execute `/solucao-documentos` para orquestrar a equipe completa ou ative qualquer agente isoladamente para regenerar apenas as respectivas páginas.

| Agente | Função |
|--------|--------|
| **Solução Documentos** | Orquestra a equipe, conduz a entrevista de 3 perguntas e calcula a seed determinística. Ativação: `/solucao-documentos` |
| **Cartógrafo** | Estrutura espacial: `arquitetura.html` (Code City 3D, Three.js), `modulos.html` (grafo force-directed em D3) e `topologia.html` (comparação lado a lado entre o sistema legado e o moderno) |
| **Analista** | Dados quantitativos: `metricas.html` (treemap, sankey, histograma e gráfico de colunas em Highcharts) e `timeline.html` (eventos extraídos de `.solucao/chronicle.md`) |
| **Narrador** | Narrativa: `glossario.html` (com busca no lado do cliente), `deck.html` (de 6 a 10 slides navegáveis) e `features/<spec>.html` (uma página por especificação SDD) |
| **Publicador** | Integração final: `index.html` com seção de destaque (hero) e selo generativo exclusivo, detecção automática dos HTMLs auxiliares gerados pelos demais agentes, validação de links e telemetria local |

A equipe inclui 5 skills compartilhadas (`solucao-arquitetura-3d`, `solucao-selo-generativo`, `solucao-highcharts-visualizer`, `solucao-especialista-d3`, `solucao-prompt-de-imagem-json`), que são instaladas automaticamente junto com ela. O resultado é um minissite estático que pode ser aberto via `file://`, sem necessidade de servidor.

### Agentes de Defeitos

Uma memória causal de defeitos nativa do repositório, organizada por **contexto** (a funcionalidade, o módulo ou o caso de uso a que o usuário se refere): cada pasta de contexto em `_solucao_bugs/<contexto>/` reúne tudo o que diz respeito àquela área (relatos anotados em `intake/`, pastas autocontidas de cada bug, inspeções e visualizações geradas, incluindo um `graph.html` clicável). Cada bug possui um registro em front matter YAML rastreável até as especificações (`SPEC ↔ CODE ↔ TEST ↔ BUG`), um plano visual de correção aprovado antes de qualquer alteração e um bloqueio `DONE.md` após o encerramento. Registrar e corrigir são atos estritamente separados.

| Agente | Função |
|--------|--------|
| **Registro de Defeitos** | Recebimento, triagem, eliminação de duplicatas, classificação e rastreabilidade inicial. Nunca realiza correções. Ativação: `/solucao-depuracao` |
| **Correção de Defeitos** | Orquestrador do ciclo de vida: mitigação, cápsula de reprodução, causa raiz baseada em evidências, dois pontos de aprovação (primeiro os testes que falham, depois o conjunto de alterações), parecer sobre a especificação com adendos versionados e política de encerramento. Ativação: `/solucao-depuracao-resolver` |
| **Debate de Defeitos** | Debate entre múltiplos agentes, com número fixo de rodadas e um juiz isolado, em três modos (`diagnosis`, `repair`, `spec`). Sempre opcional, com o custo informado previamente; harnesses externos (Codex, Gemini CLI etc.) só podem participar mediante consentimento explícito. Ativação: `/solucao-depuracao-considerar` |
| **Inspeção Detalhada** | Varredura aprofundada de uma funcionalidade problemática sob lentes especializadas (conformidade com a especificação, fluxo de dados, contratos, estados de erro, cobertura de testes e concorrência). Apenas diagnóstico; as constatações confirmadas tornam-se bugs registrados. Ativação: `/solucao-inspecao-detalhada` |
| **Grafo de Defeitos** | Regenera as visualizações derivadas: índice, catálogo compacto, matriz esparsa de relações, grafo em Mermaid com clusters e pontuação de impacto, e a matriz de rastreabilidade BUG ↔ SPEC em ambas as pontas (`_solucao_bugs/generated/` e `_solucao_sdd/traceability/bugs.md`). Ativação: `/solucao-depuracao-grafico` |

### Agentes de Qualidade de Código

Manutenção perfectiva e preventiva de código que já funciona: aprimorar a estrutura interna **sem alterar o comportamento observável** e comprovar essa preservação antes de modificar o código. Organizados por **contexto** em `_solucao_refactor/<contexto>/`, com cada transformação ancorada na essência do sistema (`soul.md`) e nas especificações confirmadas. A regra fundamental: propor uma transformação e aplicá-la são atos distintos, e nada altera o sistema legado sem a comprovação de que o comportamento foi preservado (uma **rede de segurança** composta por testes de caracterização, além de verificações de essência e de regressão). O código do projeto somente é alterado por meio de um ponto de aprovação de diff, que deve ser aprovado e reversível.

| Agente | Função |
|--------|--------|
| **Refatoração** | Orquestrador: inventaria as oportunidades de melhoria, prioriza pelo ROI real (hotpath, e não estética), direciona ao especialista adequado e executa os pontos de aprovação. Nunca aplica uma transformação. Ativação: `/solucao-refactor` |
| **Reestruturação** | Estrutura interna no nível de métodos e classes, com base no catálogo de Fowler, em pequenos passos reversíveis. Ativação: `/solucao-restructure` |
| **Modularização** | Divide um componente extenso em módulos coesos, com responsabilidades bem definidas, respeitando os limites estabelecidos pela essência do sistema. Ativação: `/solucao-modularize` |
| **Desacoplamento** | Reduz as dependências diretas (inversão de dependência, seams de Feathers e quebra de ciclos), com o acoplamento medido antes e depois. Ativação: `/solucao-decouple` |
| **Otimização** | Reduz o consumo de tempo, memória e recursos, com medição antes e depois e preservação da saída. Ativação: `/solucao-optimize` |
| **Simplificação** | Substitui uma lógica complexa por outra mais simples, com comprovação de equivalência da saída. Ativação: `/solucao-simplify` |
| **Padronização** | Aplica convenções de nomenclatura, formatação e organização com base no padrão predominante do projeto, sem jamais alterar a semântica. Ativação: `/solucao-standardize` |
| **Poda** | Remove código morto, e somente aquilo que consegue comprovar que está morto, distinguindo código morto de código suspeito de estar órfão. Ativação: `/solucao-prune` |

---

## O que é gerado

```
_solucao_sdd/
├── inventario.md              # Projeto inventário
├── dependencias.md           # Dependências with versions
├── analise-codigo.md          # Technical analysis per module
├── dicionario-dados.md        # Data dictionary
├── dominio.md                 # Glossary and business rules
├── maquina-estado.md         # State machines in Mermaid
├── permissions.md            # Permission matrix
├── arquitetura.md           # Architectural overview
├── c4-contexto.md             # C4 Diagram: Context
├── c4-conteineres.md          # C4 Diagram: Containers
├── c4-componentes.md          # C4 Diagram: Components
├── erd-complete.md           # Full ERD in Mermaid
├── confidence-report.md      # Confidence report 🟢🟡🔴
├── lacunas.md                # Lacunas identificadas
├── duvidas.md              # Questions for human validation
├── sdd/                      # Specs per component
│   └── [component].md
├── openapi/                  # API specs (if applicable)
├── user-stories/             # User stories (if applicable)
├── adrs/                     # Retroactive architectural decisions
├── flowcharts/               # Flowcharts in Mermaid
├── sequences/                # Sequence diagrams
├── ui/                       # Interface specs (Visor)
├── database/                 # Database specs (Data Master)
├── sistema-design/            # Design tokens (Design System)
├── addenda/                  # Post-delivery addenda, one per feature (Sync)
└── traceability/
    ├── spec-impact-matrix.md # Which spec impacts which
    └── code-spec-matrix.md   # Code file to corresponding spec
```

Em uma execução greenfield, o `/solucao-novo` acrescenta os seguintes itens a `_solucao_sdd/`:

```
_solucao_sdd/
├── newproject-brief.md      # Initial brief (Solucao New)
├── ideation.md              # Structured brainstorm (Ideator)
├── personas.md              # Personas with journeys (Researcher)
├── prd.md                   # Product Requirements Document (Drafter)
└── sdd/
    └── [component].md       # SDD specs with quality score (Spec SDD)
```

As funcionalidades do ciclo de evolução são gravadas em uma pasta separada, `_solucao_forward/` por padrão:

```
_solucao_forward/
└── <NNN>-<short-name>/      # Uma pasta por funcionalidade
    ├── requisitos.md
    ├── roadmap.md
    ├── investigation.md
    ├── data-delta.md
    ├── onboarding.md
    ├── interfaces/
    ├── actions.md
    ├── progress.jsonl
    ├── legacy-impact.md
    ├── regression-watch.md
    └── auditoria/
        ├── requisitos-auditoria.md
        └── cross-check.md
```

Após o `/solucao-codificacao`, o comando opcional `/solucao-sincronizar` condensa a funcionalidade entregue em `_solucao_sdd/addenda/<id-da-funcionalidade>-<nome-curto>.md`. O adendo funciona como uma ponte: mantém a extração representativa do sistema como ele é atualmente, aponta as seções de `arquitetura.md` e `dominio.md` que se desatualizaram e é marcado como substituído na próxima reextração completa. Os artefatos originais da extração nunca são editados.

Os Agentes de Ideação gravam apenas em `_solucao_sdd/brainstorms/` (uma pasta por sessão) e em `.solucao/active-ideation.json`. Eles nunca alteram o código do projeto e nunca produzem código.

A Equipe de Documentação grava apenas em `_solucao_documentos/` (minissite em HTML, totalmente offline).

Os Agentes de Defeitos gravam apenas em `_solucao_bugs/` (uma pasta por bug, além das visualizações geradas), nos adendos de especificação em `_solucao_sdd/addenda/` e no espelho gerado `_solucao_sdd/traceability/bugs.md`. As especificações originais nunca são editadas; o código do projeto só é alterado por meio de pontos de aprovação com diffs explícitos.

Os Agentes de Qualidade de Código gravam apenas em `_solucao_refactor/` (oportunidades, planos e registros de transformação por contexto). O código do projeto só é alterado mediante um diff aprovado e reversível, e somente depois que a rede de segurança comprova a preservação do comportamento.

### Confidence scale

Every statement in the specs is marked with:

| Mark | Meaning |
|------|---------|
| 🟢 CONFIRMED | Extracted directly from code — can be cited with file and line |
| 🟡 INFERRED | Deduced from patterns — may be wrong |
| 🔴 GAP | Not determinable from code — requires human validation |

---

## Supported engines

| Engine | File created | Skills path | Activation |
|--------|-------------|-------------|------------|
| Claude Code ⭐ | `CLAUDE.md` | `.claude/skills/solucao-*/` and `.agents/skills/solucao-*/` | `/solucao` |
| Codex ⭐ | `AGENTS.md` | `.agents/skills/solucao-*/` | `solucao` |
| Cursor ⭐ | `.cursorrules` | `.agents/skills/solucao-*/` | `/solucao` |
| Gemini CLI | `GEMINI.md` | `.agents/skills/solucao-*/` | `/solucao` |
| Windsurf | `.windsurfrules` | `.agents/skills/solucao-*/` | `/solucao` |
| Antigravity | `AGENTS.md` | `.agents/skills/solucao-*/` | `/solucao` |
| Kiro | (none) | `.kiro/skills/solucao-*/` and `.agents/skills/solucao-*/` | `/solucao` |
| Opencode | `AGENTS.md` | `.agents/skills/solucao-*/` | `solucao` |
| Cline | `.clinerules` | `.agents/skills/solucao-*/` | `/solucao` |
| Roo Code | `.roorules` | `.agents/skills/solucao-*/` | `/solucao` |
| GitHub Copilot | `.github/copilot-instructions.md` | `.agents/skills/solucao-*/` | `/solucao` |
| Aider | `CONVENTIONS.md` | `.agents/skills/solucao-*/` | `solucao` |
| Amazon Q Developer | `.amazonq/rules/solucao.md` | `.agents/skills/solucao-*/` | `/solucao` |

---

## Comandos da CLI

```bash
npx solucao install      # Instala o Solução no projeto
npx solucao status       # Exibe o estado atual da análise
npx solucao update       # Atualiza os agentes para a versão mais recente
npx solucao add-agent    # Adiciona um agente ao projeto
npx solucao add-engine   # Adiciona suporte a um novo motor
npx solucao uninstall    # Remove o Solução do projeto
```

O comando `update` identifica, por meio de SHA-256, os arquivos que você modificou e nunca sobrescreve personalizações.
O comando `uninstall` remove apenas os arquivos criados pelo Solução — nada do projeto legado é afetado.

---

## Estrutura interna

```
.solucao/
├── state.json          # Estado da análise entre sessões
├── config.toml         # Configuração do projeto
├── config.user.toml    # Preferências pessoais (não versionar)
├── plano.md            # Plano de exploração (editável pelo usuário)
├── version             # Versão instalada
├── contexto/
│   ├── surface.json    # Gerado pelo Explorador
│   └── modules.json    # Gerado pelo Arqueólogo
└── _config/
    ├── manifest.yaml       # Metadados da instalação
    └── files-manifest.json # Hashes SHA-256 para atualizações seguras

.agents/skills/         # Skills universais (todos os agentes compatíveis)
.claude/skills/         # Espelho para o Claude Code
```

---

## Contributing

Contributions are welcome. Open an issue to discuss before submitting a PR.

```bash
git clone https://github.com/cildefonso/solucao.git
cd solucao
npm install
```

---

## License

MIT — see [LICENSE](LICENSE) for details.
