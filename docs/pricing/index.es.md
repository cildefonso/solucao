# Pricing and Size Agents

El Team **Pricing and Size Agents** estima esfuerzo, tamaño y precio de cada feature, sobre los artefactos producidos por el pipeline Code Forward.

Marcado por defecto en el instalador.

---

## Pipeline

```
/solucao-perfil-precificacao        (una vez: perfil de cobranza)
        │
        ▼
/solucao-fins-precificacao           (por feature: T-shirt sizing estructural)
        │
        ▼
/solucao-estimativa-preco       (por feature: 3 escenarios lado a lado)
```

El `profile` corre una sola vez y se reutiliza. El `size` y el `estimate` corren por feature, después de `/solucao-pendencia`.

---

## Agentes

| Agente | Stage | Función |
|--------|-------|---------|
| `solucao-perfil-precificacao` | profile | Entrevista guiada (hasta diez preguntas) que produce el perfil de cobranza del usuario: país, moneda, seniority normalizada, tarifa por hora, markup de proyecto, régimen tributario, modelo de cobranza, perfil de cliente. |
| `solucao-fins-precificacao` | size | Lee requisitos, dudas, plan y tasks de la feature activa y produce métricas estructurales determinísticas en `size.json` y `size.md` (T-shirt sizing basado en tasks con ajuste de riesgo). |
| `solucao-estimativa-preco` | estimate | Cruza `profile.json` y `size.json` de la feature activa y produce tres escenarios educativos lado a lado: Esfuerzo, Valor, Rango de Mercado. Nunca entrega un número único como respuesta final. |

---

## Dónde caen los artefactos

```
_solucao_sdd/_pricing/
├── profile.json               (una vez, desde /solucao-perfil-precificacao)
├── profile.md
└── <feature>/
    ├── size.json              (por feature, desde /solucao-fins-precificacao)
    ├── size.md
    ├── estimate.json          (por feature, desde /solucao-estimativa-preco)
    └── estimate.md
```

Los Pricing and Size Agents nunca modifican código legado, artefactos del Discovery ni del Forward. Solo los leen y escriben dentro de `_pricing/`.
