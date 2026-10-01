# Code Forward Agents

El Team **Code Forward Agents** toma las specs producidas por el descubrimiento y conduce la evolución: desde una idea libre hasta código corriendo, siempre anclado a los artefactos del legado ya extraídos por Solucao.

Marcado por defecto en el instalador.

---

## Pipeline

```
/solucao-enviar         (orquestador, detecta la etapa y sugiere el próximo skill)
        │
        ▼
/solucao-requisitos
        │
        ▼
/solucao-clarificar           (opcional, aclara ambigüedad)
        │
        ▼
/solucao-plano            (enfoque técnico como delta sobre el legado)
        │
        ▼
/solucao-pendencia           (tareas atómicas, IDs, dependencias, paralelismo)
        │
        ▼
/solucao-auditoria           (opcional, cross-check requisitos x roadmap x actions)
/solucao-qualidade         (opcional, calidad textual del requisitos)
        │
        ▼
/solucao-codificacao          (ejecuta actions.md como código)
```

`/solucao-enviar` es el punto de entrada opcional del ciclo: observa el estado actual y dice cuál es el próximo skill. Útil cuando no recuerdas dónde te detuviste.
`/solucao-principios` corre separado, gestiona principios duraderos del proyecto.
`/solucao-resumo` intercambia la feature activa por una pausada.

---

## Agentes

| Agente | Stage | Función |
|--------|-------|---------|
| `solucao-enviar` | orchestrator | Detecta la etapa física de la feature activa en `_solucao_forward/` y sugiere el próximo skill del ciclo. No escribe artefactos, solo enruta. |
| `solucao-requisitos` | requisitos | Convierte una idea libre en un `requisitos.md` completo, anclado a los artefactos de la pipeline solucao. |
| `solucao-clarificar` | clarificar | Hasta cinco preguntas dirigidas para resolver puntos abiertos del `requisitos.md` e integrar las respuestas. |
| `solucao-plano` | plano | Esboza el enfoque técnico como delta sobre el legado: roadmap, investigation, data-delta, onboarding, interfaces. |
| `solucao-pendencia` | pendencia | Descompone el roadmap en acciones atómicas con IDs estables, dependencias y marcador de paralelismo. |
| `solucao-auditoria` | auditoria | Auditor estrictamente lector: contradicciones y lagunas entre requisitos, roadmap y actions, con severidad reportada. |
| `solucao-qualidade` | quality | Revisa la claridad de la escritura del `requisitos.md`. No verifica tests de implementación. |
| `solucao-codificacao` | codificacao | Ejecuta `actions.md` como código real, actualiza checkboxes y deja `legacy-impact.md` y `regression-watch.md`. |
| `solucao-principios` | principios | Crea y mantiene principios duraderos del proyecto, separados de los requisitos de cada feature. |
| `solucao-resumo` | resumo | Retoma una feature pausada listada en `paused-features` de `active-requisitos.json`. |

---

## Dónde caen los artefactos

Cada feature vive en su propia carpeta bajo `_solucao_forward/`. La ruta exacta se lee del campo `forward_folder` en `.solucao/state.json`.

Los Code Forward Agents nunca tocan el código legado ni los artefactos del Discovery Team. Consumen las salidas de Discovery y escriben solo dentro de la carpeta forward.
