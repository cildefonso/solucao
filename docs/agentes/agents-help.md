# Guide with analogies

Not sure which agent to call? Activate the guide:

```
/solucao-agents-help
```

It explains each agent with a real-world analogy. But since you're already here, here's the full rundown:

---

## Main menu

| Goal | Command | Team |
|---|---|---|
| Discover and document a legacy system | `/solucao` | Solucao Agents Core |
| Create a new project from an idea | `/solucao-new` | Code New Project Agents |
| Implement or evolve code from specs | `/solucao-forward` | Code Forward Agents |
| Plan a legacy migration | `/solucao-migrate` | Migration Agents |
| Generate a visual documentation mini-site | `/solucao-docs` | Documentation Agents |
| Choose the right agent | `/solucao-agents-help` | Agent guide |

Pricing and Translators use specialized commands: `/solucao-pricing-profile`, `/solucao-pricing-size`, `/solucao-pricing-estimate` and `/solucao-n8n`.

---

## Orchestrators and core agents

### 🆕 Solucao New: the product founder

The founder starts with a rough idea, investigates the problem, identifies the audience, consolidates a PRD and turns it into implementation-ready specifications.

> Use `/solucao-new` for greenfield projects. It drives `Ideator → Researcher → Drafter → Spec SDD` and hands the result to `/solucao-forward`.

### 🎼 Solucao: the orchestra conductor

A conductor doesn't play any instrument. They know the full score and tell who enters when, in what order, at what pace. Without them, each musician would play their part without connecting to the others.

> Use `/solucao` to start or resume the full analysis. It handles the sequence for you.

---

### 🗺️ Scout: the real estate agent

The agent does the first tour of the property. Doesn't open drawers, doesn't read documents, doesn't touch anything. Just maps: how many rooms, which neighborhood, what facilities exist, what's the general condition.

> Use Scout at the beginning. It generates the project inventory without diving into the code logic.

---

### ⛏️ Archaeologist: the excavator

The archaeologist digs through the terrain patiently, layer by layer. Catalogs every artifact found: size, material, location, shape. Doesn't interpret the civilization, just describes precisely what's there.

> Use the Archaeologist to analyze code module by module. Runs one module per session to conserve tokens.

---

### 🔍 Detective: Sherlock Holmes

Sherlock Holmes arrives after the archaeologist. Looks at the cataloged artifacts and asks: *"But why is this here? Who put it here? What does this reveal about who lived here?"* Doesn't excavate, interprets.

> Use the Detective after the Archaeologist. It extracts implicit business rules, reads git history like a diary, and reconstructs decisions nobody documented.

---

### 📐 Architect: the cartographer

The cartographer visits a territory and produces formal maps: floor plan, elevation map, structural plan. Someone who never set foot there can understand everything just by looking at the maps.

> Use the Architect after the Detective. It synthesizes everything into C4 diagrams, full ERD, and integration map.

---

### 📝 Writer: the notary

The notary transforms what was discovered into formal, precise, traceable contracts. Each clause has a declared confidence level. The document is a contract: an AI agent can reimplement the system from it.

> Use the Writer after the Architect. It generates SDD specs, OpenAPI, and user stories with code traceability.

---

### ⚖️ Reviewer: the spec reviewer

The Reviewer takes the Writer's contracts and tries to punch holes in them: *"This is a contradiction. This point has no proof. This rule disappears if the user does X."* Not to destroy, but to ensure what's left standing is solid.

> Use the Reviewer after the Writer. It critically reviews specs, reclassifies confidence, and raises questions for human validation.

---

### 🖼️ Visor: the forensic illustrator

The forensic illustrator works only with images. Receives screenshots of the system and faithfully reconstructs the interface: screens, forms, navigation flows. Doesn't need the system to be running. Just the photos.

> Use Visor when you have screenshots available. It documents the UI without needing access to the system.

---

### 🗄️ Data Master: the geologist

The geologist maps the underground: the layer nobody sees but that supports everything. Tables, relationships, constraints, triggers, procedures. The invisible foundation on which the application is built.

> Use Data Master when DDL, migrations, or ORM models are available.

---

### 🎨 Design System: the stylist

The stylist catalogs the wardrobe: color palette, typography, spacing, design tokens. The "fashion rules" that govern the system's appearance.

> Use Design System when CSS files, themes, or interface screenshots are available.

---

## Recommended sequence

```
Legacy project: /solucao → discovery and specifications
New project:    /solucao-new → PRD and specs → /solucao-forward
Migration:      /solucao → /solucao-migrate → /solucao-forward

Manual legacy pipeline:
Scout → Archaeologist (N sessions) → Detective → Architect → Writer → Reviewer

Optional at any phase:
Visor · Data Master · Design System · Solucao Docs
```
