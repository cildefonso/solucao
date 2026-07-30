# Desarrollando desde los specs

Una vez que Solucao ha generado todos los specs en `_solucao_sdd/`, puedes copiar esos archivos a cualquier máquina y comenzar a construir el sistema desde cero. Aquí está el orden recomendado.

---

## Antes de escribir una sola línea de código

Comienza leyendo estos tres archivos:

| Archivo | Por qué leer primero |
|---|---|
| `_solucao_sdd/confidence-report.md` | Muestra qué tiene alta confianza (verde) vs. brechas (rojo). Evita implementar algo basado en inferencias incorrectas. |
| `_solucao_sdd/gaps.md` | Lista lo que Solucao no pudo determinar. Completa manualmente antes de comenzar. |
| `_solucao_sdd/architecture.md` + diagramas C4 | Muestra el panorama general: capas, módulos, límites del sistema. |

---

## Orden de implementación (bottom-up)

```
1. database/  +  erd-complete.md                  (estructuras de datos, migraciones)
2. domain.md  +  <unit>/ de las entidades core    (reglas de negocio centrales: lee requirements.md, design.md, tasks.md de cada unit)
3. <unit>/ de los servicios ordenados por dependencia (usa dependencies.md como guía)
4. openapi/   +  contratos de API                 (si existen)
5. ui/                                            (capa de presentación al final)
```

---

## Qué unit va primero

Abre `_solucao_sdd/traceability/code-spec-matrix.md`. Lista cada unit y sus dependencias.

Implementa primero las units que no dependen de ninguna otra (hojas del árbol de dependencias), y sube hacia las units que integran múltiples componentes.

---

## Mantener la trazabilidad durante el desarrollo

Usa `_solucao_sdd/traceability/code-spec-matrix.md` como referencia durante el desarrollo para saber qué fragmento de código implementado corresponde a qué spec. Esto mantiene la trazabilidad precisa a medida que el código crece.

---

## Ver también

- [Salidas generadas](saidas/index.md): lista completa de archivos producidos por Solucao
- [Escala de confianza](escala-confianca.md): cómo interpretar los marcadores 🟢🟡🔴 en los specs
