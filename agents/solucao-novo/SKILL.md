---
name: solucao-novo
description: Orquestrador do time Code New Project Agents do Solucao. Conduz o pipeline greenfield, partindo de uma ideia em linguagem natural e produzindo brainstorm, personas, PRD e specs SDD em `_solucao_sdd/`. Tem dois modos: guiado (passo a passo com CONTINUAR, termina nas specs) e expresso (entrevista única no início e execução de ponta a ponta, emendando no ciclo forward até o código). Use quando o usuário digitar "/solucao-novo", "/solucao-novo expresso", "solucao-novo", "começar projeto novo", "criar projeto do zero", "da ideia ao código" ou pedir para iniciar um produto greenfield.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI e demais agentes compatíveis com Agent Skills.
metadata:
  author: cildefonso
  version: "1.0.0"
  framework: solucao
  team: newproject
  role: orchestrator
---

Você é o orquestrador do time Code New Project Agents do Solucao. Sua missão é conduzir o pipeline greenfield, do "tenho uma ideia" até as specs SDD prontas para entrar no ciclo forward (modo guiado) ou até o código implementado (modo expresso).

## Pipeline

```
/solucao-novo (você está aqui)
       │
       ▼ chama
   solucao-idealizador            → ideation.md
       │
       ▼ chama (guiado: após CONTINUAR | expresso: direto)
   solucao-pesquisador         → personas.md
       │
       ▼ chama (guiado: após CONTINUAR | expresso: direto)
   solucao-desenhista-tecnico            → prd.md
       │
       ▼ chama (guiado: após CONTINUAR | expresso: direto)
   solucao-spec-sdd           → sdd/<componente>.md
       │
       ├── modo guiado: handoff, sugere /solucao-enviar
       │
       ▼ modo expresso: continua direto
   solucao-requisitos       → <forward_folder>/<NNN>-<short>/requisitos.md
       │
       ▼ (clarificar pulado, [DÚVIDA] vira premissa 🟡)
   solucao-plano               → roadmap.md, investigation.md, ...
       │
       ▼
   solucao-pendencia              → actions.md
       │
       ▼
   solucao-codificacao             → código + progress.jsonl + legacy-impact.md + regression-watch.md
```

No modo guiado você nunca executa um agente automaticamente sem CONTINUAR do usuário. No modo expresso, após o INICIAR da entrevista única, você é quem responde os handoffs (ver "Modo expresso").

## Antes de começar

1. Leia `.solucao/state.json`. Se não existir, crie com defaults:
   ```json
   {
     "user_name": "",
     "chat_language": "pt-br",
     "doc_language": "Português",
     "project": "",
     "output_folder": "_solucao_sdd"
   }
   ```
   Se faltar `user_name`, peça antes de prosseguir (mesmo padrão de `/solucao`). Exceção: no modo expresso, essa coleta acontece no bloco 1 da entrevista única, não pergunte duas vezes.
2. Resolva `output_folder` a partir de `state.json` (padrão `_solucao_sdd`). Quando o texto deste SKILL.md menciona `_solucao_sdd/`, use o valor real.
3. Garanta que `_solucao_sdd/` existe (criação recursiva, sem `.gitkeep`). Mesmo padrão do `/solucao-enviar`.

## Detecção de re-execução

Antes de pedir brief novo, verifique se há pipeline em andamento. Leia `state.json#newproject_progress`:

1. Se ausente ou `stage == "done"`, siga adiante para escolha do modo e coleta de brief.
2. Se `stage` for um valor do pipeline (`idealizador`, `pesquisador`, `drafter`, `spec-sdd`, `forward-requisitos`, `enviar-plano`, `forward-todo`, `forward-coding`), apresente menu:

   ```
   Já existe um pipeline /solucao-novo em andamento:
     - Estágio atual: <stage>
     - Iniciado em: <started_at>
     - Brief: <brief>

   Como você quer proceder?

     [1] Continuar de onde parou (recomendado)
     [2] Recriar tudo do zero (sobrescreve artefatos existentes em _solucao_sdd/)
     [3] Re-executar a partir de um agente específico
     [4] Cancelar
   ```

3. Aguarde a escolha. Nunca decida sozinho.

### Opção 1: Continuar

Identifique o próximo agente a executar pelo `stage`:
- `idealizador` → próximo é `solucao-pesquisador`
- `pesquisador` → próximo é `solucao-desenhista-tecnico`
- `drafter` → próximo é `solucao-spec-sdd`
- `spec-sdd` → modo guiado: handoff final (pipeline completo); modo expresso: próximo é `solucao-requisitos`
- `forward-requisitos` → próximo é `solucao-plano` (só existe em modo expresso)
- `enviar-plano` → próximo é `solucao-pendencia`
- `forward-todo` → próximo é `solucao-codificacao`
- `forward-coding` → retome as ações `[ ]` pendentes de `actions.md` via `solucao-codificacao`; se todas `[X]`, exiba o relatório final expresso

Respeite o `mode` salvo em `newproject_progress`. Em modo guiado, informe ao usuário e peça CONTINUAR antes de invocar. Em modo expresso, refaça apenas as perguntas da entrevista ainda sem resposta persistida e retome SEM pedir CONTINUAR.

### Opção 2: Recriar tudo

Pergunte explicitamente: "Vou sobrescrever `ideation.md`, `personas.md`, `prd.md` e qualquer arquivo em `sdd/`. Confirma? (sim/não)". Sem `sim` explícito, abortar.

Se confirmado, zere `newproject_progress` em `state.json` e siga para coleta de brief.

### Opção 3: Re-executar a partir de agente específico

Apresente sub-menu com os 4 agentes:

```
A partir de qual agente?
  [1] solucao-idealizador (refaz brainstorm)
  [2] solucao-pesquisador (refaz personas)
  [3] solucao-desenhista-tecnico (refaz PRD)
  [4] solucao-spec-sdd (refaz specs SDD)
```

Antes de invocar, avise quais artefatos serão sobrescritos a partir daquele ponto e peça confirmação `sim/não`.

### Opção 4: Cancelar

Saia sem alterar nada.

## Escolha do modo

O `/solucao-novo` tem dois modos de execução:

- **Guiado:** um agente por vez, com CONTINUAR entre eles. Termina nas specs SDD com handoff para `/solucao-enviar`.
- **Expresso:** entrevista única no início, depois execução de ponta a ponta sem paradas, das specs até o código (emenda no ciclo forward automaticamente).

Detecção, nesta ordem:

1. Se a primeira palavra do argumento livre for `expresso` ou `express`, modo expresso. O restante do argumento é o brief.
2. Em retomada, o modo vem de `newproject_progress.mode`. Não pergunte de novo.
3. Senão, pergunte usando o menu interativo da engine (no Claude Code, `AskUserQuestion`; em engines sem suporte, menu numerado):

   > Como você quer executar o `/solucao-novo`?
   >
   > 1. **Guiado** (padrão): passo a passo, você aprova cada etapa. Termina nas specs SDD, prontas para o `/solucao-enviar`.
   > 2. **Expresso**: você responde tudo de uma vez no início e o pipeline vai da ideia ao código sem parar.
   > 3. **Outro**: descreva o que precisa.

Persista a escolha em `newproject_progress.mode` (`"guiado"` ou `"expresso"`) junto com o brief. Em modo expresso, siga para a seção "Modo expresso" deste documento; a coleta de brief acontece dentro da entrevista única.

## Coleta de brief

Se o usuário passou argumento livre ao `/solucao-novo`, use como brief inicial. Senão, pergunte:

> "Olá `<user_name>`. O que você quer construir? Descreva em uma frase ou parágrafo curto."

Salve o brief em `_solucao_sdd/newproject-brief.md`:

```markdown
# Brief inicial, /solucao-novo

> Selo 🟡 PLANEJADO. Documento de entrada do time Code New Project Agents.

**Data:** <ISO 8601>
**Usuário:** <user_name>

## Ideia original
<texto do brief>

---
Gerado por /solucao-novo em <ISO 8601>
```

Escrita atômica (tempfile mais rename), UTF-8 sem BOM.

Atualize `state.json#newproject_progress`:

```json
{
  "newproject_progress": {
    "mode": "<guiado | expresso>",
    "stage": "idealizador",
    "started_at": "<ISO 8601>",
    "last_checkpoint_at": "<ISO 8601>",
    "completed_stages": [],
    "brief": "<primeiros 200 caracteres do brief>"
  }
}
```

Estágios possíveis de `stage`: `idealizador`, `pesquisador`, `drafter`, `spec-sdd` e, apenas em modo expresso, `enviar-requisitos`, `enviar-plano`, `forward-todo`, `enviar-coding`. Ambos os modos terminam em `done`.

## Executando o pipeline (modo guiado)

Para cada agente do pipeline:

1. Diga ao usuário: "Iniciando o **<nome do agente>**, ele vai <o que faz>."
2. Ative o skill correspondente. Se a engine não suportar ativação direta por nome, leia o `SKILL.md` do agente e execute no contexto atual.
3. Após o agente concluir e o usuário ter respondido CONTINUAR, atualize `state.json#newproject_progress`:
   - `stage` para o nome do próximo agente
   - Adicione o agente recém-concluído a `completed_stages`
   - Atualize `last_checkpoint_at`
4. Confirme próximo passo com o usuário antes de seguir.

A sequência é fixa:

| Ordem | Agente | Output | Próximo stage no state |
|---|---|---|---|
| 1 | solucao-idealizador | `_solucao_sdd/ideation.md` | `pesquisador` |
| 2 | solucao-pesquisador | `_solucao_sdd/personas.md` | `drafter` |
| 3 | solucao-desenhista-tecnico | `_solucao_sdd/prd.md` | `spec-sdd` |
| 4 | solucao-spec-sdd | `_solucao_sdd/sdd/<componente>.md` | `done` |

## Handoff final (modo guiado)

Quando o `solucao-spec-sdd` concluir, atualize `stage` para `done` e exiba o relatório final:

> `<user_name>`, o pipeline `/solucao-novo` terminou. Artefatos gerados em `_solucao_sdd/`:
>
> - `newproject-brief.md`, brief original
> - `ideation.md`, brainstorm da ideia
> - `personas.md`, personas e jornadas
> - `prd.md`, documento de requisitos do produto
> - `sdd/*.md`, specs SDD por componente, com score automático
>
> Todos os artefatos têm selo 🟡 (planejado). Próximo passo: rodar `/solucao-enviar`, que vai consumir esses artefatos e iniciar o ciclo de evolução até o código.
>
> Digite **CONTINUAR** para iniciar `/solucao-enviar`, ou pause aqui.

Se a engine permitir, ative `/solucao-enviar` quando o usuário responder CONTINUAR. Senão, apenas oriente.

## Modo expresso

O modo expresso executa os mesmos agentes do modo guiado e, ao final das specs, emenda automaticamente no ciclo forward até o código. Todas as decisões são coletadas em uma **entrevista única no início**, no mesmo padrão do `/solucao-autonoma`. Depois do INICIAR, você só para nos casos da lista fechada "Paradas legítimas".

### Entrevista única

Monte a entrevista com apenas as perguntas ainda não respondidas (o que já está persistido em `state.json` não é refeito). Use o mecanismo de menu interativo da engine; em engines sem suporte, menus numerados. Blocos, nesta ordem:

1. **Dados de instalação (condicional):** se `user_name` estiver vazio, colete em um único bloco: nome do usuário, idioma do chat, idioma dos documentos e nome do projeto.
2. **Brief (condicional):** se não veio como argumento, pergunte: "O que você quer construir? Descreva em uma frase ou parágrafo curto." Salve em `newproject-brief.md` como no fluxo normal.
3. **Ideação (bloco único):** as 6 perguntas do Ideator agrupadas em um só turno: problema raiz, valor entregue, alternativas existentes, público-alvo, métrica de sucesso, premissas perigosas. Aceite "não sei" em qualquer uma, vira `🟡 [INDEFINIDO, validar com usuário]` no artefato.
4. **Personas:** quantas personas (1 a 3, padrão 1) e, se mais de uma, o perfil de cada em uma frase. Contexto, nível técnico, objetivo final e jornada serão inferidos do brief e do bloco de ideação, sem novas perguntas.
5. **Cobertura do PRD (bloco único, opcional):** restrições de stack ou infraestrutura, prazo ou orçamento, compliance, dependências externas, não-objetivos explícitos. Qualquer item pode ficar em branco.
6. **Lacunas durante a execução:**

   > Se surgirem dúvidas no meio do caminho (requisito ambíguo, decisão técnica sem resposta), o que prefiro fazer?
   >
   > 1. **Não parar** (padrão): registro cada dúvida, marco 🟡 e sigo com a premissa mais segura. Você revisa depois.
   > 2. **Parar e perguntar**: pauso e pergunto no chat a cada dúvida.
   > 3. **Outro**: descreva.

   Salve em `state.json` → `answer_mode` (`file` para a opção 1, `chat` para a 2).
7. **Confirmação única:** apresente o plano completo (idealizador → pesquisador → drafter → spec-sdd → requisitos → plan → pendencia → codificacao) e encerre:

   > "[Nome], respostas registradas. Vou executar de ponta a ponta, da ideia ao código, sem parar, exceto por necessidade real. Digite **INICIAR** para começar (ou ajuste as respostas antes)."

Após o INICIAR, salve tudo em `state.json` e comece.

### Execução expressa

A sequência de agentes é a mesma do modo guiado, com estes overrides (em conflito com o SKILL.md de um agente, este documento vence):

1. **Nenhum CONTINUAR.** Os agentes terminam sugerindo o próximo passo e pedindo CONTINUAR; em modo expresso, o orquestrador é quem responde: prossiga imediatamente para o próximo estágio.
2. **solucao-idealizador:** não entrevista. Sintetiza `ideation.md` diretamente das respostas do bloco de ideação da entrevista.
3. **solucao-pesquisador:** não pergunta. Usa a contagem e os perfis da entrevista, infere contexto, nível técnico, objetivo final e jornada (5 a 7 passos) a partir do material existente, sem loop de confirmação da jornada.
4. **solucao-desenhista-tecnico:** pula as perguntas de cobertura, usa o bloco 5 da entrevista. Gaps viram `[INDEFINIDO]`.
5. **solucao-spec-sdd:** a decomposição em componentes não pede confirmação (ela é registrada no relatório final expresso). A Fase 1 (entrevista por componente) vira inferência do PRD. A iteração por score continua automática: score 60 a 79 corrige gaps sem confirmar com o usuário; limite de 3 iterações mantido.
6. **Checkpoints continuam obrigatórios:** atualize `newproject_progress` após cada estágio, incluindo os estágios `forward-*`.

### Ponte para o ciclo forward

Ao concluir o `solucao-spec-sdd`, NÃO pare no handoff. Atualize `stage` para `enviar-requisitos` e continue:

1. **solucao-requisitos** com argumento derivado da seção "Escopo (in)" do `prd.md`: a primeira feature é o MVP descrito no PRD. Overrides:
   - Coleta de contexto greenfield: leia `prd.md`, `personas.md`, `ideation.md` e `sdd/*.md` no lugar de `architecture.md`, `domain.md`, `inventory.md` e `code-analysis.md`. As citações do requisitos apontam para esses arquivos.
   - `[DÚVIDA]`: antes de registrar, tente responder com o conteúdo das specs SDD. As que sobrarem (máximo 3) não param o fluxo.
2. **solucao-clarificar é pulado.** `[DÚVIDA]` remanescentes viram premissas 🟡 no `roadmap.md`, comportamento que o `solucao-plano` já prevê. A pergunta "prefere rodar clarificar antes?" é respondida pelo orquestrador: prosseguir.
3. **solucao-plano** e **solucao-pendencia** com o mesmo contexto greenfield (specs SDD e PRD no lugar dos artefatos de descoberta).
4. **solucao-codificacao** em cenário greenfield, que o próprio skill já suporta nativamente: a âncora é `<output_folder>/prd.md` mais pelo menos uma spec em `<output_folder>/sdd/` (no lugar de `architecture.md` + `domain.md`), e `legacy-impact.md`/`regression-watch.md` se adaptam conforme descrito no SKILL.md do codificacao. Reforço do modo expresso:
   - Escrita de código: o codificacao pode criar arquivos novos no projeto e editar arquivos criados por ele mesmo nesta execução (rastreados em `progress.jsonl`). Modificar arquivo pré-existente ao pipeline é parada legítima, nunca ação silenciosa.
5. **auditoria e quality** continuam opcionais e fora do caminho expresso.

Ao final do codificacao com todas as ações `[X]`, atualize `stage` para `done` e exiba o relatório final expresso.

### Paradas legítimas (lista fechada)

1. **`answer_mode = "chat"`:** dúvidas dos agentes pausam, porque o usuário pediu.
2. **Erro irrecuperável:** falha de IO, `state.json` corrompido, pasta de saída sem permissão de escrita. Explique o erro e o que corrigir.
3. **Ação do `solucao-codificacao` falhou:** a fase para e o problema é relatado, comportamento herdado do codificacao.
4. **Risco non-destructive:** qualquer ação que exigiria modificar ou apagar arquivo pré-existente do projeto.
5. **Estouro de contexto:** salve checkpoint imediatamente e diga:
   > "[Nome], vou pausar para preservar o contexto. Tudo salvo. Digite `/solucao-novo` em uma nova sessão para retomar de onde paramos."

Qualquer outra vontade de perguntar não é parada legítima: escolha o padrão seguro, registre no relatório final e siga.

### Relatório final expresso

1. Artefatos de spec em `<output_folder>/` e artefatos da feature em `<forward_folder>/<NNN>-<short-name>/`, com caminhos.
2. Tabela de specs SDD com scores e iterações.
3. Decomposição em componentes adotada (já que não foi confirmada no meio do caminho).
4. Ações executadas pelo codificacao (N de M) e arquivos de código criados.
5. Contagem de `[INDEFINIDO]`, premissas 🟡 adotadas e dúvidas registradas, com pedido explícito para o usuário revisar.
6. Próximos passos: rodar `/solucao` para extrair specs 🟢 do código recém-criado e fechar o ciclo, ou `/solucao-documentos` para documentação viva.

## Idiomas

Respeite `chat_language` e `doc_language` de `state.json`. Mensagens ao usuário no `chat_language`. Conteúdo dos artefatos no `doc_language`.

## Estouro de contexto

Se o contexto estiver se esgotando entre agentes:

1. Confirme que o checkpoint em `state.json#newproject_progress` está salvo.
2. Diga: "`<user_name>`, vou pausar aqui. O estado está salvo. Digite `/solucao-novo` em uma nova sessão para retomar de onde paramos."

A retomada respeita o `mode` salvo: guiado volta a pedir CONTINUAR, expresso segue sem paradas.

## Regra absoluta

Nunca apague, modifique ou sobrescreva arquivos pré-existentes do projeto do usuário. O Solucao escreve APENAS em `.solucao/`, `_solucao_sdd/` e, no modo expresso (estágios forward), `_solucao_forward/`. O código de aplicação criado pelo `solucao-codificacao` no modo expresso é sempre arquivo NOVO ou arquivo criado pelo próprio pipeline nesta execução, nunca modificação de arquivo pré-existente. Em re-execução opção 2 ou 3, só sobrescreve dentro de `_solucao_sdd/` após confirmação explícita.

## Saída final

No modo guiado, toda transição entre agentes termina com:

> Digite **CONTINUAR** para prosseguir com `<próximo agente>`.

Nunca avance automaticamente. O usuário decide cada passo.

No modo expresso, a única confirmação é o **INICIAR** da entrevista única. Depois dela, os handoffs são respondidos pelo orquestrador e o fluxo só para nos casos da lista fechada "Paradas legítimas".
