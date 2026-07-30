# Los agentes del Forward

Diez agentes forman el equipo **Code Forward Agents**. El orquestador (`/solucao-forward`) detecta el estado físico de la feature activa y sugiere el siguiente skill. Los otros nueve cubren el ciclo de vida desde una idea en texto libre hasta el código en ejecución.

El orquestador corre en **dos escenarios**: evolución de legado con `_solucao_sdd/` poblado, o greenfield, sin extracción todavía. En ambos casos prepara las carpetas y nunca bloquea el pipeline.

---

## Pipeline

```
Solucao Forward (orquestador, punto de entrada opcional)
        │
        ▼
Requirements → Clarify → Quality → Plan → To-Do → Audit → Coding
                (opcional)  (opcional)             (opcional)

Principles y Resume corren fuera de este flujo lineal.
```

Hay un checkpoint `CONTINUAR` entre agentes. Cada skill verifica sus propias precondiciones y se niega a correr si falta un predecesor obligatorio. `solucao-coding` es el más estricto: aborta a menos que `_solucao_sdd/` tenga un ancla de contexto, ya sea el par de legado `architecture.md` + `domain.md` (de `/solucao`) o el par greenfield `prd.md` + al menos una spec en `sdd/` (de `/solucao-new`), para mantener sólido el puente specs-código.

---

## 1. Solucao Forward (orquestador)

**Comando:** `/solucao-forward`

Mira `.solucao/state.json` y `_solucao_forward/<feature>/` para detectar la etapa física inspeccionando los artefactos en disco (no metadata). Sugiere el siguiente skill, nunca lo ejecuta automáticamente: toda transición termina con pedido de `CONTINUAR`.

Detecta greenfield (sin `_solucao_sdd/`), crea las carpetas que `/solucao` habría creado y deja que el pipeline corra sin bloqueo.

**Produce:** nada por sí solo. Solo enrutamiento.

---

## 2. Requirements

**Comando:** `/solucao-requirements`

Transforma una idea en texto libre ("quiero que el usuario exporte facturas en PDF") en un `requirements.md` completo, anclado a `_solucao_sdd/architecture.md`, `domain.md`, `state-machines.md` y al glosario. Marca puntos abiertos con `[DOUBT]`, lista gaps y registra la feature en `.solucao/active-requirements.json`.

Detecta features en curso: si otra está activa, pregunta al usuario si quiere continuar, correr en paralelo (pausando la anterior) o abandonar. Nunca decide por sí solo.

**Produce:** `requirements.md` y entrada en `active-requirements.json`.

---

## 3. Clarify

**Comando:** `/solucao-clarify`

Genera hasta cinco preguntas dirigidas para resolver marcadores `[DOUBT]`, frases vagas ("probablemente", "tal vez") y gaps obvios. Las preguntas son de opción múltiple o respuesta corta, nunca abiertas. Las respuestas se integran de vuelta en `requirements.md` bajo una sección `## Clarifications` con fecha.

**Produce:** ediciones in-place en `requirements.md`.

---

## 4. Quality

**Comando:** `/solucao-quality`

Auditor read-only de claridad textual. Pregunta: *este texto está lo suficientemente bueno como para planificar sobre él sin retrabajo?*. Categorías: claridad, completitud, terminología, cobertura de escenarios, edge cases, jerga, soluciones implícitas, alineación con `principles.md`. Veredicto: Aprobado, Aprobado con reservas o Reprobado. No verifica tests de implementación.

**Produce:** `audit/requirements-audit.md`.

---

## 5. Plan

**Comando:** `/solucao-plan`

El arquitecto de la evolución. Traduce los requirements en una propuesta técnica concreta expresada como **delta sobre el legado**, nunca una re-arquitectura completa. Cada decisión lleva un marcador de confianza (🟢 evidencia fuerte, 🟡 parcial o basada en premisas aceptadas, 🔴 débil). Los conflictos con `principles.md` se señalan, pero nunca se sobrescriben silenciosamente.

**Produce:** `roadmap.md`, `investigation.md`, `data-delta.md`, `onboarding.md`, `interfaces/*` (un archivo por contrato externo afectado).

---

## 6. To-Do

**Comando:** `/solucao-to-do`

Descompone el roadmap en acciones atómicas distribuidas en cinco fases fijas: Preparación, Tests, Core, Integración, Pulido. Cada acción recibe un ID estable (`T001`, `T002`, ..., nunca reciclados), dependencias explícitas, archivo objetivo, marcador de confianza heredado y flag `[//]` cuando puede correr en paralelo con hermanas.

**Produce:** `actions.md`.

---

## 7. Audit

**Comando:** `/solucao-audit`

Cross-check read-only entre requirements, roadmap y actions. Los hallazgos se reportan con severidad (CRITICAL, HIGH, MEDIUM, LOW), agrupados en cuatro ejes: cobertura, consistencia, coherencia con el legado (`_solucao_sdd/domain.md`, `architecture.md`) y sanidad del grafo de actions (sin ciclos, tareas paralelas no comparten archivos). El skill nunca edita los documentos analizados, ni siquiera si el usuario lo pide.

**Produce:** `audit/cross-check.md`.

---

## 8. Coding

**Comando:** `/solucao-coding`

El ejecutor. Recorre `actions.md` fase por fase, respeta el paralelismo `[//]` y las dependencias, gira checkboxes de `[ ]` a `[X]` solo en éxito y agrega una línea por action en `progress.jsonl`. Al concluir (total o parcial), escribe dos trazas para la próxima ejecución del Discovery:

- `legacy-impact.md`: qué archivos del legado fueron tocados.
- `regression-watch.md`: invariantes que deben permanecer verdaderos en la próxima extracción solucao.

**Produce:** código fuente, checkboxes actualizados en `actions.md`, `progress.jsonl`, `legacy-impact.md`, `regression-watch.md`.

---

## 9. Principles

**Comando:** `/solucao-principles`

Gestiona reglas duraderas del proyecto en `.solucao/principles.md`, separadas de los requirements de feature. Los principios son raros (típicamente menos de una vez al mes), usan números romanos (I, II, III, ...) que nunca se reciclan y los cambios se rastrean en una sección de historial. Cuando un principio cambia, el skill emite un reporte de impacto (`principles-impact-YYYYMMDD.md`) sugiriendo ajustes en templates. El humano los aplica, el skill nunca reescribe templates automáticamente.

**Produce:** `.solucao/principles.md` y `principles-impact-YYYYMMDD.md` en cada cambio.

---

## 10. Resume

**Comando:** `/solucao-resume`

Intercambia la feature activa con una de `paused-features`. Detecta la etapa física de cada feature pausada, muestra entradas huérfanas (carpeta borrada manualmente) y nunca crea features nuevas.

**Produce:** swap in-place de `active-requirements.json`. Ningún artefacto de feature es tocado.

---

## Ejecución manual

`/solucao-forward` es el punto de entrada recomendado cuando no recuerdas dónde paró la feature activa. Pero cada skill puede activarse de forma independiente:

```
/solucao-forward                 # detecta etapa y sugiere siguiente skill
/solucao-requirements <idea>     # nueva feature desde idea en texto libre
/solucao-clarify                 # resuelve marcadores [DOUBT] en requirements.md
/solucao-quality                 # audita claridad textual (read-only)
/solucao-plan                    # delta sobre legado desde requirements.md
/solucao-to-do                   # acciones atómicas desde roadmap.md
/solucao-audit                   # cross-check entre los tres docs (read-only)
/solucao-coding                  # ejecuta actions.md
/solucao-principles              # gestiona reglas duraderas
/solucao-resume                  # cambia a una feature pausada
```

Hooks declarados en `.solucao/hooks.yml` (slots `before-<stage>` y `after-<stage>`) se aplican en toda transición.
