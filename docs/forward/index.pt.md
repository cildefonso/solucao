# Code Forward Agents

O Team **Code Forward Agents** pega as specs produzidas pela descoberta e conduz a evolução: de uma ideia livre até código rodando, sempre ancorado nos artefatos do legado já extraídos pelo Solucao.

Marcado por padrão no instalador.

---

## Pipeline

```
/solucao-enviar         (orquestrador, detecta o estágio e sugere o próximo skill)
        │
        ▼
/solucao-requisitos
        │
        ▼
/solucao-clarificar           (opcional, esclarece ambiguidade)
        │
        ▼
/solucao-plano            (abordagem técnica como delta sobre o legado)
        │
        ▼
/solucao-pendencia           (tarefas atômicas, IDs, dependências, paralelismo)
        │
        ▼
/solucao-auditoria           (opcional, cross-check requisitos x roadmap x actions)
/solucao-qualidade         (opcional, qualidade textual do requisitos)
        │
        ▼
/solucao-codificacao          (executa actions.md em código)
```

`/solucao-enviar` é o ponto de entrada opcional do ciclo: olha o estado atual e diz qual o próximo skill. Útil quando você não lembra onde parou.
`/solucao-principios` roda separado, gerencia princípios duradouros do projeto.
`/solucao-resumo` troca a feature ativa por uma pausada.

---

## Agentes

| Agente | Stage | Função |
|--------|-------|--------|
| `solucao-enviar` | orchestrator | Detecta o estágio físico da feature ativa em `_solucao_forward/` e sugere o próximo skill do ciclo. Não escreve artefatos, só roteia. |
| `solucao-requisitos` | requisitos | Transforma uma ideia livre em `requisitos.md` completo, ancorado nos artefatos da pipeline solucao. |
| `solucao-clarificar` | clarificar | Até cinco perguntas dirigidas para resolver pontos abertos do `requisitos.md` e integrar as respostas. |
| `solucao-plano` | plano | Esboça a abordagem técnica como delta sobre o legado: roadmap, investigation, data-delta, onboarding, interfaces. |
| `solucao-pendencia` | pendencia | Decompõe o roadmap em ações atômicas com IDs estáveis, dependências e marcador de paralelismo. |
| `solucao-auditoria` | auditoria | Auditor estritamente leitor: contradições e lacunas entre requisitos, roadmap e actions, severidade reportada. |
| `solucao-qualidade` | quality | Revisa a clareza da escrita do `requisitos.md`. Não verifica testes de implementação. |
| `solucao-codificacao` | codificacao | Executa `actions.md` em código real, atualiza checkboxes e deixa `legacy-impact.md` e `regression-watch.md`. |
| `solucao-principios` | principios | Cria e mantém princípios duradouros do projeto, separados dos requisitos de cada feature. |
| `solucao-resumo` | resumo | Retoma uma feature pausada listada em `paused-features` de `active-requisitos.json`. |

---

## Onde os artefatos vão parar

Cada feature mora em sua própria pasta sob `_solucao_forward/`. O caminho exato sai do campo `forward_folder` em `.solucao/state.json`.

Os Code Forward Agents jamais tocam no código legado nem nos artefatos do Discovery Team. Consomem as saídas de Discovery e escrevem apenas dentro da pasta forward.
