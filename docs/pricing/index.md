# Pricing and Size Agents

The **Pricing and Size Agents** Team estimates effort, size and price for each feature, on top of the artifacts produced by the Code Forward pipeline.

Pre-checked in the installer.

---

## Pipeline

```
/solucao-pricing-profile        (one-time setup: billing profile)
        │
        ▼
/solucao-pricing-size           (per feature: structural T-shirt sizing)
        │
        ▼
/solucao-pricing-estimate       (per feature: 3 scenarios side by side)
```

`profile` runs once and is reused. `size` and `estimate` run for each feature, after `/solucao-to-do`.

---

## Agents

| Agent | Stage | Role |
|-------|-------|------|
| `solucao-pricing-profile` | profile | Guided interview (up to ten questions) that produces the user's billing profile: country, currency, normalized seniority, hourly rate, project markup, tax regime, billing model, client profile. |
| `solucao-pricing-size` | size | Reads requirements, doubts, plan and tasks of the active feature and produces deterministic structural metrics in `size.json` and `size.md` (T-shirt sizing based on tasks plus risk adjustment). |
| `solucao-pricing-estimate` | estimate | Combines `profile.json` and `size.json` of the active feature to produce three educational scenarios side by side: Effort, Value, Market Range. Never delivers a single number as the final answer. |

---

## Where artifacts land

```
_solucao_sdd/_pricing/
├── profile.json               (one-time, from /solucao-pricing-profile)
├── profile.md
└── <feature>/
    ├── size.json              (per feature, from /solucao-pricing-size)
    ├── size.md
    ├── estimate.json          (per feature, from /solucao-pricing-estimate)
    └── estimate.md
```

The Pricing and Size Agents never modify legacy code, Discovery artifacts or Forward artifacts. They only read those and write inside `_pricing/`.
