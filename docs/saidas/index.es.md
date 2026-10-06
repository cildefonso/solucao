# Salidas generadas

Todo lo que Solucao produce va a la carpeta `_solucao_sdd/`. El proyecto heredado nunca es tocado.

El conjunto de artefactos generados depende del **nivel de documentación** elegido al inicio del análisis:

| Leyenda | Nivel |
|---------|-------|
| *(todos)* | Generado en los 3 niveles |
| *(completo+)* | Solo en los niveles `completo` y `detalhado` |
| *(detalhado)* | Solo en el nivel `detalhado` |

---

## Estructura completa

```
_solucao_sdd/
├── inventario.md              # Inventario del proyecto — todos
├── dependencias.md           # Dependencias con versiones — todos
├── analise-codigo.md          # Análisis técnico por módulo — todos
├── dicionario-dados.md        # Diccionario completo de datos — completo+
├── dominio.md                 # Glosario y reglas de negocio — todos
├── maquina-estado.md         # Máquinas de estado en Mermaid — completo+
├── permissions.md            # Matriz de permisos — completo+
├── arquitetura.md           # Visión arquitectónica general — todos
├── c4-contexto.md             # Diagrama C4: Contexto — todos
├── c4-conteineres.md          # Diagrama C4: Containers — completo+
├── c4-componentes.md          # Diagrama C4: Componentes — completo+
├── erd-complete.md           # ERD completo en Mermaid — completo+
├── deployment.md             # Diagrama de infraestructura — detalhado
├── confidence-report.md      # Reporte de confianza 🟢🟡🔴 — todos
├── lacunas.md                   # Brechas sin resolver — completo+
├── duvidas.md              # Preguntas para validación humana — todos
├── sdd/                      # Specs por componente — todos
├── openapi/                  # Specs de API — completo+
├── user-stories/             # User stories — completo+
├── adrs/                     # Decisiones arquitectónicas retroactivas — completo+
├── flowcharts/               # Diagramas de flujo en Mermaid — completo+
├── ui/                       # Specs de interfaz (Visor)
├── database/                 # Specs de base de datos (Data Master)
├── sistema-design/            # Tokens de diseño (Design System)
└── traceability/
    ├── spec-impact-matrix.md # Qué spec impacta a cuál — completo+
    └── code-spec-matrix.md   # Archivo de código a spec correspondiente — completo+
```

---

## Trazabilidad

**`traceability/code-spec-matrix.md`:** mapea cada archivo de código a su spec correspondiente, con el nivel de cobertura.

**`traceability/spec-impact-matrix.md`:** mapea qué componente impacta a cuál. Antes de cambiar algo, sabes el radio de impacto del cambio.

---

## Siguiente paso

Specs en mano? Consulta [Desarrollando desde los specs](../desenvolvendo-com-specs.md) para el orden recomendado de construcción del sistema.
