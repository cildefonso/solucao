# The Forward agents

Ten agents make up the Code Forward Agents Team. The orchestrator (`/solucao-enviar`) detects the physical stage of the active feature and suggests the next skill. The other nine cover the lifecycle from a free-form idea to running code.

The orchestrator runs in **two scenarios**: evolution of a legacy with `_solucao_sdd/` populated, or greenfield, where there is no extraction yet. In both cases it prepares the folders and never blocks the pipeline.

---

## Pipeline

```
Solucao Forward (orchestrator, optional entry point)
        │
        ▼
Requirements → Clarify → Quality → Plan → To-Do → Audit → Coding
                (optional)  (optional)             (optional)

Principles and Resume run outside this linear flow.
```

There is a `CONTINUAR` checkpoint between agents. Each skill verifies its own preconditions and refuses to run if a required predecessor is missing. `solucao-codificacao` is the strictest: it aborts unless `_solucao_sdd/` holds a context anchor, either the legacy pair `arquitetura.md` + `dominio.md` (from `/solucao`) or the greenfield pair `prd.md` + at least one spec in `sdd/` (from `/solucao-novo`), to keep the specs-to-code bridge solid.

---

## 1. Solucao Forward (orchestrator)

**Command:** `/solucao-enviar`

Looks at `.solucao/state.json` and `_solucao_forward/<feature>/` to detect the physical stage by inspecting the artifacts on disk (not metadata). Suggests the next skill, never executes it automatically: every transition ends with a `CONTINUAR` request.

Detects greenfield (no `_solucao_sdd/`), creates the folders that would have been created by `/solucao`, and lets the pipeline run without blocking.

**Produces:** nothing on its own. Pure routing.

---

## 2. Requirements

**Command:** `/solucao-requisitos`

Turns a free-form idea ("I want users to export their invoices as PDF") into a complete `requisitos.md`, anchored to `_solucao_sdd/arquitetura.md`, `dominio.md`, `maquina-estado.md` and the glossary. Marks open points with `[DOUBT]`, lists gaps and registers the feature in `.solucao/active-requisitos.json`.

Detects in-progress features: if another one is active, asks the user to continue, run in parallel (pausing the previous one) or abandon. Never decides on its own.

**Produces:** `requisitos.md` and an entry in `active-requisitos.json`.

---

## 3. Clarify

**Command:** `/solucao-clarificar`

Generates up to five targeted questions to clear `[DOUBT]` markers, vague phrases ("probably", "maybe") and obvious gaps. Questions are multiple choice or short answer, never open. Answers are integrated back into `requisitos.md` under a dated `## Clarifications` section.

**Produces:** in-place edits to `requisitos.md`.

---

## 4. Quality

**Command:** `/solucao-qualidade`

Read-only auditor of writing clarity. Asks: *is this prose good enough to plan against without rework?*. Categories: clarity, completeness, terminology, scenario coverage, edge cases, jargon, implicit solutions, alignment with `principios.md`. Verdict: Approved, Approved with reservations or Rejected. Does not check implementation tests.

**Produces:** `auditoria/requisitos-auditoria.md`.

---

## 5. Plan

**Command:** `/solucao-plano`

The evolution architect. Translates requirements into a concrete technical proposal expressed as a **delta over the legacy**, never a full re-architecture. Each decision carries a confidence marker (🟢 strong evidence, 🟡 partial or based on accepted assumptions, 🔴 weak). Conflicts with `principios.md` are flagged but never silently overridden.

**Produces:** `roadmap.md`, `investigation.md`, `data-delta.md`, `onboarding.md`, `interfaces/*` (one file per affected external contract).

---

## 6. To-Do

**Command:** `/solucao-pendencia`

Decomposes the roadmap into atomic actions across five fixed phases: Preparation, Tests, Core, Integration, Polish. Each action gets a stable ID (`T001`, `T002`, ..., never recycled), explicit dependencies, a target file, an inherited confidence marker and a `[//]` flag when it can run in parallel with siblings.

**Produces:** `actions.md`.

---

## 7. Audit

**Command:** `/solucao-auditoria`

Read-only cross-check between requirements, roadmap and actions. Findings are reported with severity (CRITICAL, HIGH, MEDIUM, LOW), grouped along four axes: coverage, consistency, coherence with the legacy (`_solucao_sdd/dominio.md`, `arquitetura.md`) and sanity of the actions graph (no cycles, parallel tasks do not share files). The skill never edits the analyzed documents, even if the user asks.

**Produces:** `auditoria/cross-check.md`.

---

## 8. Coding

**Command:** `/solucao-codificacao`

The executor. Walks `actions.md` phase by phase, respects `[//]` parallelism and dependencies, flips checkboxes from `[ ]` to `[X]` only on success and appends one line per action to `progress.jsonl`. On completion (full or partial) writes two trails for the next Discovery run:

- `legacy-impact.md`: which legacy files were touched.
- `regression-watch.md`: invariants that must remain true on the next Solucao extraction.

**Produces:** source code, updated checkboxes in `actions.md`, `progress.jsonl`, `legacy-impact.md`, `regression-watch.md`.

---

## 9. Principles

**Command:** `/solucao-principios`

Manages durable project rules in `.solucao/principios.md`, separated from feature requirements. Principles are rare (typically less than once a month), use roman numerals (I, II, III, ...) that are never recycled and changes are tracked in a history section. When a principle changes, the skill emits an impact report (`principios-impact-YYYYMMDD.md`) suggesting template adjustments. The human applies them, the skill never auto-rewrites templates.

**Produces:** `.solucao/principios.md` and `principios-impact-YYYYMMDD.md` on each change.

---

## 10. Resume

**Command:** `/solucao-resumo`

Swaps the active feature with one from `paused-features`. Detects the physical stage of each paused feature, surfaces any orphaned entries (folder deleted manually) and never creates new features.

**Produces:** in-place swap of `active-requisitos.json`. No feature artifacts touched.

---

## Running manually

`/solucao-enviar` is the recommended entry point when you do not remember where the active feature stopped. But each skill can be activated standalone:

```
/solucao-enviar                 # detect stage and suggest next skill
/solucao-requisitos <idea>     # new feature from a free-form idea
/solucao-clarificar                 # resolve [DOUBT] markers in requisitos.md
/solucao-qualidade                 # audit writing clarity (read-only)
/solucao-plano                    # delta over legacy from requisitos.md
/solucao-pendencia                   # atomic actions from roadmap.md
/solucao-auditoria               # cross-check between the three docs (read-only)
/solucao-codificacao                  # execute actions.md
/solucao-principios              # manage durable rules
/solucao-resumo                  # swap with a paused feature
```

Hooks declared in `.solucao/hooks.yml` (`before-<stage>` and `after-<stage>` slots) apply on every transition.
