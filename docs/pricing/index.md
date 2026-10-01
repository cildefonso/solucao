# Pricing and Size Agents

The **Pricing and Size Agents** Team estimates effort, size and price for each feature, on top of the artifacts produced by the Code Forward pipeline.

Pre-checked in the installer.

---

## Pipeline

```
/solucao-perfil-precificacao        (one-time setup: billing profile)
        │
        ▼
/solucao-fins-precificacao           (per feature: structural T-shirt sizing)
        │
        ▼
/solucao-estimativa-preco       (per feature: 3 scenarios side by side)
```

`profile` runs once and is reused. `size` and `estimate` run for each feature, after `/solucao-pendencia`.

---

## Agents

| Agent | Stage | Role |
|-------|-------|------|
| `solucao-perfil-precificacao` | profile | Guided interview (up to ten questions) that produces the user's billing profile: country, currency, normalized seniority, hourly rate, project markup, tax regime, billing model, client profile. |
| `solucao-fins-precificacao` | size | Reads requirements, doubts, plan and tasks of the active feature and produces deterministic structural metrics in `size.json` and `size.md` (T-shirt sizing based on tasks plus risk adjustment). |
| `solucao-estimativa-preco` | estimate | Combines `profile.json` and `size.json` of the active feature to produce three educational scenarios side by side: Effort, Value, Market Range. Never delivers a single number as the final answer. |

---

## Where artifacts land

```
_solucao_sdd/_pricing/
├── profile.json               (one-time, from /solucao-perfil-precificacao)
├── profile.md
└── <feature>/
    ├── size.json              (per feature, from /solucao-fins-precificacao)
    ├── size.md
    ├── estimate.json          (per feature, from /solucao-estimativa-preco)
    └── estimate.md
```

The Pricing and Size Agents never modify legacy code, Discovery artifacts or Forward artifacts. They only read those and write inside `_pricing/`.
