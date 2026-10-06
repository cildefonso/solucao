# Generated outputs

Everything Solucao produces goes to the `_solucao_sdd/` folder (or whatever name you configure in `config.toml`). The legacy project is never touched.

The set of artifacts generated depends on the **documentation level** chosen at the start of the analysis:

| Legend | Level |
|--------|-------|
| *(all)* | Generated at all 3 levels |
| *(complete+)* | Only at `complete` and `detailed` levels |
| *(detailed)* | Only at `detailed` level |

---

## Full structure

```
_solucao_sdd/
├── inventario.md              # Project inventory — all levels
├── dependencias.md           # Dependencies with versions — all levels
├── analise-codigo.md          # Technical analysis per module — all levels
├── dicionario-dados.md        # Complete data dictionary — complete+
├── dominio.md                 # Glossary and business rules — all levels
├── maquina-estado.md         # State machines in Mermaid — complete+
├── permissions.md            # Permission matrix — complete+
├── arquitetura.md           # General architectural overview — all levels
├── c4-contexto.md             # C4 Diagram: Context — all levels
├── c4-conteineres.md          # C4 Diagram: Containers — complete+
├── c4-componentes.md          # C4 Diagram: Components — complete+
├── erd-complete.md           # Full ERD in Mermaid — complete+
├── deployment.md             # Infrastructure diagram — detailed only
├── confidence-report.md      # Confidence report 🟢🟡🔴 — all levels
├── lacunas.md                   # Lacunas não resolvidas — completar+
├── duvidas.md              # Human validation questions — all levels
├── sdd/                      # Specs per component — all levels
│   └── [component].md
│
├── openapi/                  # API specs — complete+
│   └── [api].yaml
│
├── user-stories/             # User stories — complete+
│   └── [flow].md
│
├── adrs/                     # Retroactive architectural decisions — complete+
│   └── [number]-[title].md
│
├── flowcharts/               # Mermaid flowcharts — complete+
│   └── [module].md
│
├── ui/                       # Interface specs (Visor)
│   ├── inventario.md
│   ├── flow.md
│   └── screens/
│       └── [screen].md
│
├── database/                 # Database specs (Data Master)
│   ├── erd.md
│   ├── dicionario-dados.md
│   ├── relationships.md
│   ├── business-rules.md
│   └── procedures.md
│
├── sistema-design/            # Design tokens (Design System)
│   ├── color-palette.md
│   ├── typography.md
│   ├── spacing.md
│   ├── tokens.md
│   └── sistema-design.md
│
└── traceability/
    ├── spec-impact-matrix.md # Which spec impacts which — complete+
    └── code-spec-matrix.md   # Code file to corresponding spec — complete+
```

---

## Traceability

Two files connect everything:

**`traceability/code-spec-matrix.md`:** maps each code file to its corresponding spec, with coverage level. You know what's covered and what isn't.

**`traceability/spec-impact-matrix.md`:** maps which component impacts which. Before changing something, you know the blast radius of the change.

---

## What not to commit

Suggested `.gitignore` to avoid versioning Solucao outputs alongside code (unless you want to):

```gitignore
# Solucao outputs (optional: remove if you want to version the specs)
_solucao_sdd/

# Personal Solucao configuration (never commit)
.solucao/config.user.toml
```

---

## Next step

Specs in hand? See [Developing from specs](../desenvolvendo-com-specs.md) for the recommended order to build the system.
