# Reconstructor

**Command:** `/solucao-reconstructor`
**Role:** independent agent (outside the Discovery pipeline)

---

## 🧱 The bottom-up builder

When the specs already exist, the Reconstructor can rebuild the entire system from them, one task at a time. It reads only what it needs at each step, executes a single task per session, and pauses, so a long reconstruction never consumes more tokens than necessary.

---

## What it does

The Reconstructor turns the Solucao specs into an **executable reconstruction plan** and then implements each task on demand, bottom-up.

It runs in two modes:

1. **Planning mode** (the first time it's invoked): reads a small set of files, infers the dependency tree, and produces `reconstruction-plan.md` with the full task list. It picks the order by dependency depth: schema and core entities first, leaves of the dependency tree before their dependents, API layer and user flows last.
2. **Execution mode** (every subsequent invocation): picks the next unchecked task in the plan, reads only the files that task declares it needs, implements the task, marks it as done and stops.

If a finished `migration/` folder exists, the Reconstructor asks whether to rebuild from the **original specs** (faithful to the legacy) or from the **migration specs** (new system on the target stack), and tags the plan accordingly.

---

## Why bottom-up

Components without dependencies first, then everything above them. This avoids stubs, scaffolds, and rework: every layer rests on something that already exists.

## Why one task per session

Token preservation. Every task carries only the context it needs. You can pause and resume at any time without rebuilding context, and any agent can pick up the next task without re-reading the whole project.

---

## What it reads (planning)

- `.solucao/state.json` (project metadata, if present)
- `_solucao_sdd/gaps.md` (when available)
- `_solucao_sdd/confidence-report.md` (when available)
- `_solucao_sdd/architecture.md`
- `_solucao_sdd/dependencies.md`
- `_solucao_sdd/traceability/code-spec-matrix.md` (when available)
- `_solucao_sdd/migration/handoff.md` (when a migration is complete)

Unit-level files (`<unit>/requirements.md`, `design.md`, `tasks.md`) are not read during planning, only during execution of the corresponding task.

---

## What it produces

| File | Content |
|------|---------|
| `_solucao_sdd/reconstruction-plan.md` | Full bottom-up task list with `Reads:` and `Done when:` per task, plus pre-flight alerts mapped from `gaps.md` |

During execution, the Reconstructor writes the actual code in the target project (according to `paradigm_decision.md`/`target_architecture.md` when the source is the migration). Each finished task gets checked off in `reconstruction-plan.md`.

---

## When to use it

- After `/solucao` is complete and you want to reimplement the legacy from scratch under the original specs.
- After `/solucao-migrate` is complete and you want to materialize the new system from the migration specs.
- As a recovery path: you can pause anytime and resume later without restarting the context.

---

## How it connects

```
/solucao  →  specs (_solucao_sdd/)
                  │
                  ▼
/solucao-reconstructor  →  reconstruction-plan.md (one-time)  →  code, one task at a time
```

It is **independent of the main pipeline**: never blocks `/solucao`, `/solucao-forward` or `/solucao-migrate`. It is invoked separately when you choose to rebuild.
