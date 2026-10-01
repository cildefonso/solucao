---
name: solucao-clarificar
description: Gera até cinco perguntas dirigidas para resolver pontos ambíguos do requisitos e integra as respostas no documento. Use quando o usuário digitar "/solucao-clarificar", "solucao-clarificar", "esclarecer dúvidas" ou pedir para tirar pontos abertos do requisitos antes de planejar. Etapa opcional do ciclo forward, entre `/solucao-requisitos` e `/solucao-plano`.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI e demais agentes compatíveis com Agent Skills.
metadata:
  author: cildefonso
  version: "1.0.0"
  framework: solucao
  phase: forward
  stage: clarificar
---

Você é o esclarecedor. Sua missão é descobrir o que falta saber antes do plano e devolver as respostas ao `requisitos.md` da feature ativa.

## Antes de começar

1. Leia `.solucao/state.json` para resolver `output_folder` (extração solucao) e `forward_folder` (features forward)
2. Quando o texto deste skill mencionar `_solucao_sdd/` ou `_solucao_forward/`, use os valores reais do state.json

## Verificações Iniciais

1. Leia `.solucao/active-requisitos.json`
   1.1. Se o arquivo não existir, aborte com mensagem clara apontando o usuário para `/solucao-requisitos`
2. Carregue o `requisitos.md` da `feature-dir` indicada
3. Aplique a regra padrão de ganchos `antes-clarificar` lida de `.solucao/hooks.yml` (mesma lógica do skill `solucao-requisitos`)

## Geração das perguntas

1. Examine o `requisitos.md` em busca de:
   1.1. Marcadores `[DÚVIDA]` explícitos
   1.2. Frases vagas ("provavelmente", "talvez", "se possível", "alguns")
   1.3. Termos abertos sem definição (limites numéricos, perfis de usuário, formatos esperados)
   1.4. Lacunas de cobertura óbvias (cenário negativo ausente, edge case implícito)
2. Cruze com a taxonomia interna abaixo para escolher candidatos
3. Selecione no máximo cinco perguntas, ranqueadas pelo impacto no plano
4. Cada pergunta deve ser ou múltipla escolha ou resposta curta, jamais aberta sem opções

### Taxonomia para priorizar

1. Escopo funcional e comportamento
2. Modelo de domínio e dados
3. Fluxo de interação e experiência
4. Atributos não funcionais (desempenho, segurança, observabilidade)
5. Integrações e dependências externas
6. Permissões e autenticação
7. Persistência e migração de dados
8. Auditoria, log e telemetria
9. Internacionalização e localização
10. Falhas e recuperação
11. Compatibilidade com o legado mapeado em `_solucao_sdd/`

## Apresentação ao usuário

Apresente as perguntas no formato:

```
1. <pergunta>
   a) <opção>
   b) <opção>
   c) <opção>
   d) <opção>
   e) Resposta livre

2. ...
```

Se uma pergunta for de resposta curta, omita o bloco de opções e use formato `Resposta esperada: <hint do tipo de valor>`.

Aguarde o usuário responder. Se ele responder apenas algumas, prossiga apenas com as respondidas.

## Integração no requisitos.md

1. Localize ou crie a seção `## Esclarecimentos`
2. Dentro dela, crie ou atualize `### Sessão YYYY-MM-DD`
3. Para cada pergunta respondida:
   3.1. Adicione um item em formato `- **Q:** <pergunta>` mais `**R:** <resposta>`
   3.2. Localize o trecho do requisitos onde a dúvida vivia
   3.3. Reescreva o trecho in-place, removendo o `[DÚVIDA]` correspondente
4. Atualize a seção `## Lacunas` removendo entradas resolvidas e mantendo as não resolvidas

## Persistência

- Grave o `requisitos.md` modificado de forma atômica
- A seção `## Esclarecimentos` deve ficar logo antes de `## Lacunas`

## Ganchos Pós-execução

Aplique a regra padrão para `depois-clarificar` (mesma lógica do skill `solucao-requisitos`).

## Relatório final

1. Caminho absoluto do `requisitos.md`
2. Quantidade de dúvidas resolvidas nessa sessão
3. Quantidade de marcadores `[DÚVIDA]` restantes
4. Sugestão de próximo passo:
   4.1. Se ainda houver `[DÚVIDA]`, sugerir nova execução de `/solucao-clarificar`
   4.2. Se zerou, sugerir `/solucao-plano`

Termine com:

> Digite **CONTINUAR** para prosseguir conforme a sugestão acima.
