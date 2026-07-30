<!--
  Template: metricas.html
  Produtor: solucao-docs-analyst
  Skill invocada: highcharts-visualizer
  Page ID: metricas
  Categoria solucao: diagram
  Dados consumidos: assets/data/metrics.json

  Marcadores:
  - HEAD_EXTRAS: <script src="assets/vendor/highcharts.js"></script>
                 + <script src="assets/vendor/highcharts-accessibility.js"></script>
                 + <script src="assets/vendor/highcharts-exporting.js"></script>
                 + <script src="assets/vendor/highcharts-treemap.js"></script>
                 + <script src="assets/vendor/highcharts-sankey.js"></script>
                 (todos baixados pelo Publisher via vendor-pins.yaml,
                  highcharts@11.4.8)
  - CHART_TREEMAP: container do treemap LOC
  - CHART_COMPLEXITY: container das barras top 20
  - CHART_HISTOGRAM: container do histograma
  - CHART_SANKEY: container do sankey de dependências
  - SCRIPTS: monta os charts a partir de window.RV_DATA.metrics (sem fetch local)
-->

<!-- PAYLOAD_START -->
<section class="solucao-doc-dashboard" data-layout="grid-2x2">
    <article class="solucao-doc-chart">
        <h2>LOC por pasta</h2>
        <div id="chart-treemap"><!-- CHART_TREEMAP --></div>
    </article>
    <article class="solucao-doc-chart">
        <h2>Top 20 complexidade</h2>
        <div id="chart-complexity"><!-- CHART_COMPLEXITY --></div>
    </article>
    <article class="solucao-doc-chart">
        <h2>Distribuição de tamanho</h2>
        <div id="chart-histogram"><!-- CHART_HISTOGRAM --></div>
    </article>
    <article class="solucao-doc-chart">
        <h2>Fluxo de dependências</h2>
        <div id="chart-sankey"><!-- CHART_SANKEY --></div>
    </article>
</section>
<!-- PAYLOAD_END -->
