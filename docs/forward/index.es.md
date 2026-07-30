# Code Forward Agents

El Team **Code Forward Agents** toma las specs producidas por el descubrimiento y conduce la evolución: desde una idea libre hasta código corriendo, siempre anclado a los artefactos del legado ya extraídos por Solucao.

Marcado por defecto en el instalador.

---

## Pipeline

```
/solucao-forward         (orquestador, detecta la etapa y sugiere el próximo skill)
        │
        ▼
/solucao-requirements
        │
        ▼
/solucao-clarify           (opcional, aclara ambigüedad)
        │
        ▼
/solucao-plan            (enfoque técnico como delta sobre el legado)
        │
        ▼
/solucao-to-do           (tareas atómicas, IDs, dependencias, paralelismo)
        │
        ▼
/solucao-audit           (opcional, cross-check requirements x roadmap x actions)
/solucao-quality         (opcional, calidad textual del requirements)
        │
        ▼
/solucao-coding          (ejecuta actions.md como código)
```

`/solucao-forward` es el punto de entrada opcional del ciclo: observa el estado actual y dice cuál es el próximo skill. Útil cuando no recuerdas dónde te detuviste.
`/solucao-principles` corre separado, gestiona principios duraderos del proyecto.
`/solucao-resume` intercambia la feature activa por una pausada.

---

## Agentes

| Agente | Stage | Función |
|--------|-------|---------|
| `solucao-forward` | orchestrator | Detecta la etapa física de la feature activa en `_solucao_forward/` y sugiere el próximo skill del ciclo. No escribe artefactos, solo enruta. |
| `solucao-requirements` | requirements | Convierte una idea libre en un `requirements.md` completo, anclado a los artefactos de la pipeline solucao. |
| `solucao-clarify` | clarify | Hasta cinco preguntas dirigidas para resolver puntos abiertos del `requirements.md` e integrar las respuestas. |
| `solucao-plan` | plan | Esboza el enfoque técnico como delta sobre el legado: roadmap, investigation, data-delta, onboarding, interfaces. |
| `solucao-to-do` | to-do | Descompone el roadmap en acciones atómicas con IDs estables, dependencias y marcador de paralelismo. |
| `solucao-audit` | audit | Auditor estrictamente lector: contradicciones y lagunas entre requirements, roadmap y actions, con severidad reportada. |
| `solucao-quality` | quality | Revisa la claridad de la escritura del `requirements.md`. No verifica tests de implementación. |
| `solucao-coding` | coding | Ejecuta `actions.md` como código real, actualiza checkboxes y deja `legacy-impact.md` y `regression-watch.md`. |
| `solucao-principles` | principles | Crea y mantiene principios duraderos del proyecto, separados de los requisitos de cada feature. |
| `solucao-resume` | resume | Retoma una feature pausada listada en `paused-features` de `active-requirements.json`. |

---

## Dónde caen los artefactos

Cada feature vive en su propia carpeta bajo `_solucao_forward/`. La ruta exacta se lee del campo `forward_folder` en `.solucao/state.json`.

Los Code Forward Agents nunca tocan el código legado ni los artefactos del Discovery Team. Consumen las salidas de Discovery y escriben solo dentro de la carpeta forward.
