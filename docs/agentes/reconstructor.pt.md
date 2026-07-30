# Reconstructor

**Comando:** `/solucao-reconstructor`
**Papel:** agente independente (fora do pipeline de Descoberta)

---

## 🧱 O construtor bottom-up

Quando as specs já existem, o Reconstructor consegue reconstruir todo o sistema a partir delas, uma tarefa por vez. Ele lê apenas o necessário em cada passo, executa uma única tarefa por sessão, e pausa, assim uma reconstrução longa nunca consome mais tokens do que o necessário.

---

## O que ele faz

O Reconstructor transforma as specs do Solucao em um **plano de reconstrução executável** e depois implementa cada tarefa sob demanda, bottom-up.

Roda em dois modos:

1. **Modo de planejamento** (primeira vez que é invocado): lê um conjunto pequeno de arquivos, infere a árvore de dependências e produz o `reconstruction-plan.md` com a lista completa de tarefas. A ordem é escolhida por profundidade de dependência: schema e entidades-núcleo primeiro, folhas da árvore antes de seus dependentes, camada de API e fluxos de usuário por último.
2. **Modo de execução** (toda invocação seguinte): pega a próxima tarefa não marcada no plano, lê apenas os arquivos que a tarefa declara que precisa, implementa, marca como concluída e para.

Se existir uma pasta `migration/` finalizada, o Reconstructor pergunta se deve reconstruir a partir das **specs originais** (fiel ao legado) ou das **specs da migração** (sistema novo na stack alvo), e marca o plano de acordo.

---

## Por que bottom-up

Componentes sem dependências primeiro, depois tudo o que vem acima. Isso evita stubs, andaimes e retrabalho: toda camada se apoia em algo que já existe.

## Por que uma tarefa por sessão

Preservação de tokens. Cada tarefa carrega apenas o contexto que precisa. Você pode pausar e retomar a qualquer momento sem reconstruir contexto, e qualquer agente pode pegar a próxima tarefa sem reler o projeto inteiro.

---

## O que ele lê (planejamento)

- `.solucao/state.json` (metadados do projeto, se houver)
- `_solucao_sdd/gaps.md` (quando disponível)
- `_solucao_sdd/confidence-report.md` (quando disponível)
- `_solucao_sdd/architecture.md`
- `_solucao_sdd/dependencies.md`
- `_solucao_sdd/traceability/code-spec-matrix.md` (quando disponível)
- `_solucao_sdd/migration/handoff.md` (quando existe migração concluída)

Arquivos de nível de unit (`<unit>/requirements.md`, `design.md`, `tasks.md`) não são lidos no planejamento, só na execução da tarefa correspondente.

---

## O que ele produz

| Arquivo | Conteúdo |
|---------|----------|
| `_solucao_sdd/reconstruction-plan.md` | Lista completa de tarefas bottom-up com `Lê:` e `Pronto quando:` por tarefa, mais alertas pré-voo mapeados de `gaps.md` |

Durante a execução, o Reconstructor escreve o código de fato no projeto alvo (de acordo com `paradigm_decision.md`/`target_architecture.md` quando a fonte é a migração). Cada tarefa concluída é marcada no `reconstruction-plan.md`.

---

## Quando usar

- Depois que o `/solucao` terminou e você quer reimplementar o legado do zero sob as specs originais.
- Depois que o `/solucao-migrate` terminou e você quer materializar o sistema novo a partir das specs da migração.
- Como caminho de recuperação: pausa quando quiser e retoma depois sem reiniciar o contexto.

---

## Como se conecta

```
/solucao  →  specs (_solucao_sdd/)
                  │
                  ▼
/solucao-reconstructor  →  reconstruction-plan.md (uma vez)  →  código, uma tarefa por vez
```

Ele é **independente do pipeline principal**: nunca bloqueia `/solucao`, `/solucao-forward` ou `/solucao-migrate`. É invocado separadamente quando você escolhe reconstruir.
