<!--
  Template: modulos.html
  Produtor: solucao-docs-mapper
  Skill invocada: especialista-d3 (modo force-directed)
  Page ID: modulos
  Categoria solucao: diagram
  Dados consumidos: assets/data/modules.json, assets/data/deps.json

  Marcadores:
  - D3_CANVAS: SVG do force-directed
  - SIDEBAR: filtros (linguagem, tipo, força)
  - HEAD_EXTRAS: <script src="assets/vendor/d3.v7.min.js"></script>
                 (baixado pelo Publisher via vendor-pins.yaml, d3@7.8.5 IIFE)
  - SCRIPTS: monta o force-directed a partir de window.RV_DATA.modules e
             window.RV_DATA.deps (sem fetch local)
-->

<!-- PAYLOAD_START -->
<section class="solucao-doc-graph-stage" data-mode="force-directed">
    <svg id="d3-canvas" class="solucao-doc-d3-canvas" aria-label="Mapa de módulos">
        <!-- D3_CANVAS -->
    </svg>
</section>

<details class="solucao-doc-graph-legend">
    <summary>Legenda</summary>
    <ul>
        <li>Nó: módulo. Tamanho proporcional ao LOC.</li>
        <li>Aresta: dependência. Espessura proporcional ao peso.</li>
        <li>Nó vermelho: faz parte de um ciclo detectado.</li>
    </ul>
</details>
<!-- PAYLOAD_END -->
