# Code Forward Agents

O Team **Code Forward Agents** pega as specs produzidas pela descoberta e conduz a evolução: de uma ideia livre até código rodando, sempre ancorado nos artefatos do legado já extraídos pelo Solucao.

Marcado por padrão no instalador.

---

## Pipeline

```
/solucao-forward         (orquestrador, detecta o estágio e sugere o próximo skill)
        │
        ▼
/solucao-requirements
        │
        ▼
/solucao-clarify           (opcional, esclarece ambiguidade)
        │
        ▼
/solucao-plan            (abordagem técnica como delta sobre o legado)
        │
        ▼
/solucao-to-do           (tarefas atômicas, IDs, dependências, paralelismo)
        │
        ▼
/solucao-audit           (opcional, cross-check requirements x roadmap x actions)
/solucao-quality         (opcional, qualidade textual do requirements)
        │
        ▼
/solucao-coding          (executa actions.md em código)
```

`/solucao-forward` é o ponto de entrada opcional do ciclo: olha o estado atual e diz qual o próximo skill. Útil quando você não lembra onde parou.
`/solucao-principles` roda separado, gerencia princípios duradouros do projeto.
`/solucao-resume` troca a feature ativa por uma pausada.

---

## Agentes

| Agente | Stage | Função |
|--------|-------|--------|
| `solucao-forward` | orchestrator | Detecta o estágio físico da feature ativa em `_solucao_forward/` e sugere o próximo skill do ciclo. Não escreve artefatos, só roteia. |
| `solucao-requirements` | requirements | Transforma uma ideia livre em `requirements.md` completo, ancorado nos artefatos da pipeline solucao. |
| `solucao-clarify` | clarify | Até cinco perguntas dirigidas para resolver pontos abertos do `requirements.md` e integrar as respostas. |
| `solucao-plan` | plan | Esboça a abordagem técnica como delta sobre o legado: roadmap, investigation, data-delta, onboarding, interfaces. |
| `solucao-to-do` | to-do | Decompõe o roadmap em ações atômicas com IDs estáveis, dependências e marcador de paralelismo. |
| `solucao-audit` | audit | Auditor estritamente leitor: contradições e lacunas entre requirements, roadmap e actions, severidade reportada. |
| `solucao-quality` | quality | Revisa a clareza da escrita do `requirements.md`. Não verifica testes de implementação. |
| `solucao-coding` | coding | Executa `actions.md` em código real, atualiza checkboxes e deixa `legacy-impact.md` e `regression-watch.md`. |
| `solucao-principles` | principles | Cria e mantém princípios duradouros do projeto, separados dos requisitos de cada feature. |
| `solucao-resume` | resume | Retoma uma feature pausada listada em `paused-features` de `active-requirements.json`. |

---

## Onde os artefatos vão parar

Cada feature mora em sua própria pasta sob `_solucao_forward/`. O caminho exato sai do campo `forward_folder` em `.solucao/state.json`.

Os Code Forward Agents jamais tocam no código legado nem nos artefatos do Discovery Team. Consomem as saídas de Discovery e escrevem apenas dentro da pasta forward.
