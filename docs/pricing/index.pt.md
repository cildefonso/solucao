# Pricing and Size Agents

O Team **Pricing and Size Agents** estima esforço, tamanho e preço de cada feature, sobre os artefatos produzidos pelo pipeline Code Forward.

Marcado por padrão no instalador.

---

## Pipeline

```
/solucao-perfil-precificacao        (uma vez: perfil de cobrança)
        │
        ▼
/solucao-fins-precificacao           (por feature: T-shirt sizing estrutural)
        │
        ▼
/solucao-estimativa-preco       (por feature: 3 cenários lado a lado)
```

O `profile` roda uma única vez e é reutilizado. Já o `size` e o `estimate` rodam por feature, depois de `/solucao-pendencia`.

---

## Agentes

| Agente | Stage | Função |
|--------|-------|--------|
| `solucao-perfil-precificacao` | profile | Entrevista guiada (até dez perguntas) que produz o perfil de cobrança do usuário: país, moeda, senioridade normalizada, taxa hora, markup de projeto, regime tributário, modelo de cobrança, perfil de cliente. |
| `solucao-fins-precificacao` | size | Lê requisitos, dúvidas, plano e tasks da feature ativa e produz métricas estruturais determinísticas em `size.json` e `size.md` (T-shirt sizing baseado em tasks com ajuste de risco). |
| `solucao-estimativa-preco` | estimate | Cruza `profile.json` e `size.json` da feature ativa e produz três cenários educativos lado a lado: Esforço, Valor, Faixa de Mercado. Jamais entrega número único como resposta final. |

---

## Onde os artefatos vão parar

```
_solucao_sdd/_pricing/
├── profile.json               (uma vez, vindo de /solucao-perfil-precificacao)
├── profile.md
└── <feature>/
    ├── size.json              (por feature, de /solucao-fins-precificacao)
    ├── size.md
    ├── estimate.json          (por feature, de /solucao-estimativa-preco)
    └── estimate.md
```

Os Pricing and Size Agents jamais modificam código legado, artefatos do Discovery ou do Forward. Apenas leem esses e escrevem dentro de `_pricing/`.
