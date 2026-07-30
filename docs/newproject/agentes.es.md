# Los agentes del greenfield

Cinco agentes forman el equipo **Code New Project Agents**. El orquestador (`/solucao-new`) conduce los otros cuatro en secuencia fija. Cada agente lee lo que el anterior produjo y añade su propio artefacto.

---

## Pipeline

```
Solucao New (orquestador)
        │
        ▼
Ideator → Researcher → Drafter → Spec SDD
```

Hay un checkpoint `CONTINUAR` entre agentes. El orquestador nunca avanza por sí solo.

---

## 1. Solucao New (orquestador)

**Comando:** `/solucao-new`

Lee el brief inicial (pasado inline o preguntado de forma interactiva), guarda `_solucao_sdd/newproject-brief.md`, conduce los cuatro agentes funcionales en orden fijo y registra checkpoint en `state.json#newproject_progress` después de cada etapa.

Detecta re-ejecución: si ya existe un pipeline en curso, pregunta si quiere continuar, recrear o re-ejecutar desde un agente específico.

**Produce:** `_solucao_sdd/newproject-brief.md` y el estado del orquestador en `state.json#newproject_progress`.

---

## 2. Ideator

**Comando:** `/solucao-ideator`

Brainstorm estructurado con seis preguntas divergentes: problema raíz, valor entregado, alternativas, público objetivo bruto, métricas de éxito, premisas peligrosas. Hace una pregunta por vez (cuando el motor no soporta agrupar bien), espera la respuesta antes de continuar y nunca colapsa las preguntas en un único prompt.

**Produce:** `_solucao_sdd/ideation.md`.

---

## 3. Researcher

**Comando:** `/solucao-researcher`

Transforma el público objetivo bruto de `ideation.md` en 1 a 3 personas estructuradas con jornadas (entrada, fricción, desenlace). El usuario elige cuántas personas; el agente solo sugiere según la amplitud de la descripción del público.

**Produce:** `_solucao_sdd/personas.md`.

---

## 4. Drafter

**Comando:** `/solucao-drafter`

Sintetiza ideation y personas en un PRD completo: problema, métricas de éxito, alcance, no-objetivos, restricciones, riesgos, preguntas abiertas. Actúa como sintetizador, no como entrevistador: extrae todo lo que puede de las dos fuentes y hace como máximo dos preguntas de cobertura para llenar los gaps más críticos. Lo que quede indefinido se marca con `🟡 [INDEFINIDO, validar con usuario]`.

**Produce:** `_solucao_sdd/prd.md`.

---

## 5. Spec SDD

**Comando:** `/solucao-spec-sdd`

Descompone el PRD en componentes lógicos y escribe una spec SDD por componente, con score automático de calidad (0 a 100) y análisis de gaps. La metodología es **RFC Pragmático más LLM-First**: estructurada como un RFC (Problem / Goals / Design / Edge Cases), pero optimizada para ser consumida por humanos y por agentes de IA.

Ese agente es una versión **vendored** de la skill global `sdd-spec`: vive nativamente dentro de Solucao, lee `prd.md` como fuente primaria, escribe en `_solucao_sdd/sdd/`, marca cada spec con el sello 🟡 (planificado) y, al concluir, hace handoff a `/solucao-forward`.

También se puede usar de forma independiente: evaluando una spec existente o generando una spec única a partir de cualquier entrada que el usuario pase.

**Produce:** `_solucao_sdd/sdd/<componente>.md` (uno por componente).

---

## Ejecución manual

Casi nunca necesitas llamar a un agente aislado. `/solucao-new` orquesta todo. Pero si un agente falló o quieres rehacer una etapa:

```
/solucao-new                    # detecta pipeline en curso, ofrece Continuar / Recrear / Re-ejecutar
/solucao-ideator                # independiente, lee newproject-brief.md
/solucao-researcher             # independiente, lee ideation.md
/solucao-drafter                # independiente, lee ideation.md más personas.md
/solucao-spec-sdd               # independiente, lee prd.md o cualquier fuente que pase el usuario
```

Cada agente independiente verifica sus propias precondiciones y aborta con un mensaje claro apuntando al artefacto que falta.
