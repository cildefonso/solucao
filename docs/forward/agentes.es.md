# Los agentes del Forward

Diez agentes forman el equipo **Code Forward Agents**. El orquestador (`/solucao-enviar`) detecta el estado físico de la feature activa y sugiere el siguiente skill. Los otros nueve cubren el ciclo de vida desde una idea en texto libre hasta el código en ejecución.

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

Hay un checkpoint `CONTINUAR` entre agentes. Cada skill verifica sus propias precondiciones y se niega a correr si falta un predecesor obligatorio. `solucao-codificacao` es el más estricto: aborta a menos que `_solucao_sdd/` tenga un ancla de contexto, ya sea el par de legado `arquitetura.md` + `dominio.md` (de `/solucao`) o el par greenfield `prd.md` + al menos una spec en `sdd/` (de `/solucao-novo`), para mantener sólido el puente specs-código.

---

## 1. Solucao Forward (orquestador)

**Comando:** `/solucao-enviar`

Mira `.solucao/state.json` y `_solucao_forward/<feature>/` para detectar la etapa física inspeccionando los artefactos en disco (no metadata). Sugiere el siguiente skill, nunca lo ejecuta automáticamente: toda transición termina con pedido de `CONTINUAR`.

Detecta greenfield (sin `_solucao_sdd/`), crea las carpetas que `/solucao` habría creado y deja que el pipeline corra sin bloqueo.

**Produce:** nada por sí solo. Solo enrutamiento.

---

## 2. Requirements

**Comando:** `/solucao-requisitos`

Transforma una idea en texto libre ("quiero que el usuario exporte facturas en PDF") en un `requisitos.md` completo, anclado a `_solucao_sdd/arquitetura.md`, `dominio.md`, `maquina-estado.md` y al glosario. Marca puntos abiertos con `[DOUBT]`, lista gaps y registra la feature en `.solucao/active-requisitos.json`.

Detecta features en curso: si otra está activa, pregunta al usuario si quiere continuar, correr en paralelo (pausando la anterior) o abandonar. Nunca decide por sí solo.

**Produce:** `requisitos.md` y entrada en `active-requisitos.json`.

---

## 3. Clarify

**Comando:** `/solucao-clarificar`

Genera hasta cinco preguntas dirigidas para resolver marcadores `[DOUBT]`, frases vagas ("probablemente", "tal vez") y gaps obvios. Las preguntas son de opción múltiple o respuesta corta, nunca abiertas. Las respuestas se integran de vuelta en `requisitos.md` bajo una sección `## Clarifications` con fecha.

**Produce:** ediciones in-place en `requisitos.md`.

---

## 4. Quality

**Comando:** `/solucao-qualidade`

Auditor read-only de claridad textual. Pregunta: *este texto está lo suficientemente bueno como para planificar sobre él sin retrabajo?*. Categorías: claridad, completitud, terminología, cobertura de escenarios, edge cases, jerga, soluciones implícitas, alineación con `principios.md`. Veredicto: Aprobado, Aprobado con reservas o Reprobado. No verifica tests de implementación.

**Produce:** `auditoria/requisitos-auditoria.md`.

---

## 5. Plan

**Comando:** `/solucao-plano`

El arquitecto de la evolución. Traduce los requisitos en una propuesta técnica concreta expresada como **delta sobre el legado**, nunca una re-arquitectura completa. Cada decisión lleva un marcador de confianza (🟢 evidencia fuerte, 🟡 parcial o basada en premisas aceptadas, 🔴 débil). Los conflictos con `principios.md` se señalan, pero nunca se sobrescriben silenciosamente.

**Produce:** `roadmap.md`, `investigation.md`, `data-delta.md`, `onboarding.md`, `interfaces/*` (un archivo por contrato externo afectado).

---

## 6. To-Do

**Comando:** `/solucao-pendencia`

Descompone el roadmap en acciones atómicas distribuidas en cinco fases fijas: Preparación, Tests, Core, Integración, Pulido. Cada acción recibe un ID estable (`T001`, `T002`, ..., nunca reciclados), dependencias explícitas, archivo objetivo, marcador de confianza heredado y flag `[//]` cuando puede correr en paralelo con hermanas.

**Produce:** `actions.md`.

---

## 7. Audit

**Comando:** `/solucao-auditoria`

Cross-check read-only entre requisitos, roadmap y actions. Los hallazgos se reportan con severidad (CRITICAL, HIGH, MEDIUM, LOW), agrupados en cuatro ejes: cobertura, consistencia, coherencia con el legado (`_solucao_sdd/dominio.md`, `arquitetura.md`) y sanidad del grafo de actions (sin ciclos, tareas paralelas no comparten archivos). El skill nunca edita los documentos analizados, ni siquiera si el usuario lo pide.

**Produce:** `auditoria/cross-check.md`.

---

## 8. Coding

**Comando:** `/solucao-codificacao`

El ejecutor. Recorre `actions.md` fase por fase, respeta el paralelismo `[//]` y las dependencias, gira checkboxes de `[ ]` a `[X]` solo en éxito y agrega una línea por action en `progress.jsonl`. Al concluir (total o parcial), escribe dos trazas para la próxima ejecución del Discovery:

- `legacy-impact.md`: qué archivos del legado fueron tocados.
- `regression-watch.md`: invariantes que deben permanecer verdaderos en la próxima extracción solucao.

**Produce:** código fuente, checkboxes actualizados en `actions.md`, `progress.jsonl`, `legacy-impact.md`, `regression-watch.md`.

---

## 9. Principles

**Comando:** `/solucao-principios`

Gestiona reglas duraderas del proyecto en `.solucao/principios.md`, separadas de los requisitos de feature. Los principios son raros (típicamente menos de una vez al mes), usan números romanos (I, II, III, ...) que nunca se reciclan y los cambios se rastrean en una sección de historial. Cuando un principio cambia, el skill emite un reporte de impacto (`principios-impact-YYYYMMDD.md`) sugiriendo ajustes en templates. El humano los aplica, el skill nunca reescribe templates automáticamente.

**Produce:** `.solucao/principios.md` y `principios-impact-YYYYMMDD.md` en cada cambio.

---

## 10. Resume

**Comando:** `/solucao-resumo`

Intercambia la feature activa con una de `paused-features`. Detecta la etapa física de cada feature pausada, muestra entradas huérfanas (carpeta borrada manualmente) y nunca crea features nuevas.

**Produce:** swap in-place de `active-requisitos.json`. Ningún artefacto de feature es tocado.

---

## Ejecución manual

`/solucao-enviar` es el punto de entrada recomendado cuando no recuerdas dónde paró la feature activa. Pero cada skill puede activarse de forma independiente:

```
/solucao-enviar                 # detecta etapa y sugiere siguiente skill
/solucao-requisitos <idea>     # nueva feature desde idea en texto libre
/solucao-clarificar                 # resuelve marcadores [DOUBT] en requisitos.md
/solucao-qualidade                 # audita claridad textual (read-only)
/solucao-plano                    # delta sobre legado desde requisitos.md
/solucao-pendencia                   # acciones atómicas desde roadmap.md
/solucao-auditoria               # cross-check entre los tres docs (read-only)
/solucao-codificacao                  # ejecuta actions.md
/solucao-principios              # gestiona reglas duraderas
/solucao-resumo                  # cambia a una feature pausada
```

Hooks declarados en `.solucao/hooks.yml` (slots `before-<stage>` y `after-<stage>`) se aplican en toda transición.
