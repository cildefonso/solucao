---
name: solucao-plano
description: Esboça a abordagem técnica como delta sobre o legado, gerando roadmap, investigation, data-delta, onboarding e interfaces da feature ativa. Use quando o usuário digitar "/solucao-plano", "solucao-plano", "esboçar plano técnico" ou pedir para virar requisitos em desenho de solução. Terceiro skill do ciclo forward, depois de `/solucao-requisitos` e (opcionalmente) `/solucao-clarificar`.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI e demais agentes compatíveis com Agent Skills.
metadata:
  author: cildefonso
  version: "1.0.0"
  framework: solucao
  phase: forward
  stage: plano
---

Você é o arquiteto de evolução do Solucao. Sua missão é traduzir o `requisitos.md` da feature ativa numa proposta técnica concreta, expressa como delta sobre o que já existe no legado.

## Antes de começar

1. Leia `.solucao/state.json` para resolver `output_folder` e `forward_folder`
2. Use os valores reais nos lugares onde o texto mencionar `_solucao_sdd/` ou `_solucao_forward/`

## Verificações Iniciais

1. Leia `.solucao/active-requisitos.json`
   1.1. Se ausente, aborte com mensagem apontando para `/solucao-requisitos`
2. Carregue o `requisitos.md` da `feature-dir`
   2.1. Se o documento ainda tiver marcadores `[DÚVIDA]`, avise o usuário e pergunte se ele prefere rodar `/solucao-clarificar` antes
   2.2. Se o usuário confirmar que quer prosseguir mesmo com dúvidas, cada `[DÚVIDA]` vira premissa explícita no `roadmap.md`, com aviso visível
3. Aplique ganchos `angtes-plano` da forma padrão (mesma lógica do skill `solucao-requisitos`)

## Coleta de contexto técnico

Leia os artefatos da pipeline solucao nesta ordem, ignorando os que não existirem:

1. `_solucao_sdd/arquitetura.md` (componentes, dependências internas)
2. `_solucao_sdd/c4-contexto.md` (fronteiras externas)
3. `_solucao_sdd/maquina-estado.md` (máquinas de estado afetadas)
4. `_solucao_sdd/dependencias.md` (bibliotecas usadas)
5. `_solucao_sdd/analise-codigo.md`, mas apenas as seções dos componentes citados no requisitos
6. `_solucao_sdd/addenda/*.md` (adendos vigentes de features já entregues, criados pelo `/solucao-sincronizar`, com deltas que a extração ainda não absorveu)
7. `.solucao/principios.md` (princípios obrigatórios)

Anote quais arquivos serão tocados pela mudança proposta. Essa lista vai virar parte do `legacy-impact.md` quando o `/solucao-codificacao` rodar mais tarde, então registre-a em rascunho mental.

## Verificação de princípios

Para cada princípio em `principios.md`:

1. Avalie se a feature respeita o princípio
2. Se houver conflito, escreva o conflito numa seção `## Princípios Aplicados` do `roadmap.md`
3. NUNCA reescreva ou atenue um princípio aqui, isso é tarefa do `/solucao-principios`

## Geração dos artefatos

Carregue o template em `.solucao/templates/roadmap-template.md` e gere os arquivos abaixo na `feature-dir`:

| Arquivo | Conteúdo esperado |
|---------|-------------------|
| `roadmap.md` | resumo da abordagem, princípios aplicados, decisões técnicas, delta arquitetural, delta de dados, delta de contratos, plano de migração, riscos, critério de pronto |
| `investigation.md` | pesquisa de fundo, alternativas avaliadas, links para fontes externas, padrões aplicáveis |
| `data-delta.md` | diff conceitual sobre o modelo extraído em `_solucao_sdd/`, novos campos, campos removidos, migrações necessárias |
| `onboarding.md` | passo a passo executável para um humano que vai testar a feature pela primeira vez |
| `interfaces/<nome>.md` | um arquivo por contrato externo afetado (HTTP, fila, gRPC, GraphQL), descreve request, response, erros, idempotência, timeouts |

Quando a feature não tocar contratos externos, omita o diretório `interfaces/`.

## Regras de redação

- Escreva o `roadmap.md` em forma de delta, jamais redescreva a arquitetura inteira do legado
- Cite componentes do `_solucao_sdd/` por nome literal e arquivo de origem
- Marque cada decisão técnica com 🟢 / 🟡 / 🔴 conforme a confidência sobre a fonte
- Se uma decisão depender de uma `[DÚVIDA]` aceita como premissa, use 🟡

## Persistência

- Grave todos os artefatos com escrita atômica
- Crie `feature-dir/interfaces/` apenas se houver pelo menos um arquivo dentro

## Ganchos Pós-execução

Aplique `depois-plano` da forma padrão.

## Relatório final

1. Caminhos absolutos dos artefatos gerados
2. Lista de princípios em conflito, se houver
3. Lista de premissas adotadas a partir de marcadores `[DÚVIDA]` não resolvidos
4. Sugestão de próximo passo: `/solucao-pendencia` (ou `/solucao-auditoria` se houver desconfiança)

Termine com:

> Digite **CONTINUAR** para prosseguir conforme a sugestão acima.